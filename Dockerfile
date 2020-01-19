FROM ubuntu:18.04

RUN apt-get update -qq && \
    apt-get install git python python-pip software-properties-common -y
RUN add-apt-repository -y ppa:team-gcc-arm-embedded/ppa && \
    apt-get update && \
    apt-get install gcc-arm-embedded cmake ninja-build srecord libssl-dev -y
RUN pip install yotta git+https://github.com/liftoff/pyminifier

ENV MICROBIT_MICROPYTHON_HASH=a92ca9b1f907c07a01116b0eb464ca4743a28bf1

WORKDIR /
RUN git clone -b master https://github.com/bbcmicrobit/micropython microbit-micropython && \
    cd microbit-micropython && git reset --hard ${MICROBIT_MICROPYTHON_HASH} && cd -
RUN MICROPYTHON_HASH=$(sed -n '3p' microbit-micropython/inc/genhdr/mpversion.h | cut -d\" -f2) && \
    git clone -b master https://github.com/micropython/micropython micropython && \
    cd micropython && git reset --hard ${MICROPYTHON_HASH} && cd -

# initialize micropython repo
WORKDIR /microbit-micropython
RUN yt target bbc-microbit-classic-gcc-nosd && \
    yt up

# generate qstrhdr
RUN python tools/makeversionhdr.py microbitversion.h && \
    mv microbitversion.h inc/genhdr && \
    ./tools/makeqstrhdr.sh

# enable frozen and bytecoded modules
RUN sed -i '1s/^/#define MICROPY_QSTR_EXTRA_POOL (mp_qstr_frozen_const_pool)\n/' /microbit-micropython/inc/microbit/mpconfigport.h && \
    sed -i '2s/^/#define MICROPY_MODULE_FROZEN_MPY (1)\n/' /microbit-micropython/inc/microbit/mpconfigport.h && \
    sed -i '3s/^/#define MICROPY_PERSISTENT_CODE_LOAD (1)\n/' /microbit-micropython/inc/microbit/mpconfigport.h

WORKDIR /microbit-micropython
# remove the last 6 lines that contain mp_lexer_new_from_file function
RUN head -n -6 source/microbit/filesystem.c > tmp && mv tmp source/microbit/filesystem.c

# and add 2 other functions to the end of it (used to enable the use of mpy files)
RUN echo '\n\
void mp_reader_new_file(mp_reader_t *reader, const char *filename) {\n\
    file_descriptor_obj *fd = microbit_file_open(filename, strlen(filename), false, false);\n\
    if (fd == NULL) {\n\
        mp_raise_OSError(MP_ENOENT);\n\
    }\n\
    reader->data = fd;\n\
    reader->readbyte = file_read_byte;\n\
    reader->close = (void(*)(void*))microbit_file_close;\n\
}\n\
\n\
mp_lexer_t *mp_lexer_new_from_file(const char *filename) {\n\
    mp_reader_t reader;\n\
    mp_reader_new_file(&reader, filename);\n\
    return mp_lexer_new(qstr_from_str(filename), reader);\n\
}\n' >> source/microbit/filesystem.c

# Allow use of pin 5 and 11 as digital or analog pin
COPY source/microbit/microbitpin.cpp /microbit-micropython/source/microbit/

# build tool to produce bytecodes of python scripts
WORKDIR /micropython/mpy-cross
RUN make && cp ./mpy-cross /usr/bin

# create the bytecode for our modules
WORKDIR /tmp
COPY *.py ./
RUN for module in $(ls *.py); do pyminifier $module > tmp.py || exit 1; rm $module && mv tmp.py $module; done
RUN for module in $(ls *.py); do mpy-cross $module || exit 1; done

# generate the c code of our module and place it in the right dir to be compiled
RUN python /micropython/tools/mpy-tool.py -f -q /microbit-micropython/inc/genhdr/qstrdefs.preprocessed.h *.mpy > /microbit-micropython/source/py/frozen_module.c

# compile the firmware
WORKDIR /microbit-micropython
RUN make all

# print out the number of bytes used by the firmware
RUN stat --printf='%s' build/bbc-microbit-classic-gcc-nosd/source/microbit-micropython.bin > /tmp/usedspace.txt
