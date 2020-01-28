#!/bin/sh

podman build -t micropython-makerbit .
podman rm makerbit || true
podman run --name makerbit micropython-makerbit
mkdir build || true
podman cp makerbit:/microbit-micropython/build/firmware.hex build/makerbit-python.hex
podman cp makerbit:/tmp/usedspace.txt build/makerbit-python-usedspace.txt
podman rm makerbit
podman rmi micropython-makerbit
echo "Successfully completed."
