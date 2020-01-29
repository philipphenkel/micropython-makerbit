# microbit-module: touch@0.0.1
# MPR121 Touch Sensor Module

"""
Copyright (c) 2020 Roger Wagner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from microbit import i2c
from micropython import const

_MAKERBIT_MPR121 = const(0x5A) # MakerBit MPR121


# CalibrationLock
_BaselineTrackingOn = const(0b00)
_BaselineTrackingOff = const(0b01)
_BaselineTrackingAndInitializeFirst5MSB = const(0b10)
_BaselineTrackingAndInitialize = const(0b11)


# Touch
_TOUCH_DISABLED = const(0b0000)
_TOUCH_ELE_0 = const(0b0001)
_TOUCH_ELE_0_TO_1 = const(0b0010)
_TOUCH_ELE_0_TO_2 = const(0b0011)
_TOUCH_ELE_0_TO_3 = const(0b0100)
_TOUCH_ELE_0_TO_4 = const(0b0101)
_TOUCH_ELE_0_TO_5 = const(0b0110)
_TOUCH_ELE_0_TO_6 = const(0b0111)
_TOUCH_ELE_0_TO_7 = const(0b1000)
_TOUCH_ELE_0_TO_8 = const(0b1001)
_TOUCH_ELE_0_TO_9 = const(0b1010)
_TOUCH_ELE_0_TO_10 = const(0b1011)
_TOUCH_ELE_0_TO_11 = const(0b1100)


# Proximity
_PROXMITY_DISABLED = const(0b00)
_PROXMITY_ELE0_TO_1 = const(0b01)
_PROXMITY_ELE_0_TO_3 = const(0b10)
_PROXMITY_ELE_0_TO_11 = const(0b11)


# Config register
_MHDR = const(0x2b)
_NHDR = const(0x2c)
_NCLR = const(0x2d)
_FDLR = const(0x2e)
_MHDF = const(0x2f)
_NHDF = const(0x30)
_NCLF = const(0x31)
_FDLF = const(0x32)
_NHDT = const(0x33)
_NCLT = const(0x34)
_FDLT = const(0x35)
_MHDPROXR = const(0x36)
_NHDPROXR = const(0x37)
_NCLPROXR = const(0x38)
_FDLPROXR = const(0x39)
_MHDPROXF = const(0x3a)
_NHDPROXF = const(0x3b)
_NCLPROXF = const(0x3c)
_FDLPROXF = const(0x3d)
_NHDPROXT = const(0x3e)
_NCLPROXT = const(0x3f)
_FDLPROXT = const(0x40)
_E0TTH = const(0x41)
_E0RTH = const(0x42)
_E1TTH = const(0x43)
_E1RTH = const(0x44)
_E2TTH = const(0x45)
_E2RTH = const(0x46)
_E3TTH = const(0x47)
_E3RTH = const(0x48)
_E4TTH = const(0x49)
_E4RTH = const(0x4a)
_E5TTH = const(0x4b)
_E5RTH = const(0x4c)
_E6TTH = const(0x4d)
_E6RTH = const(0x4e)
_E7TTH = const(0x4f)
_E7RTH = const(0x50)
_E8TTH = const(0x51)
_E8RTH = const(0x52)
_E9TTH = const(0x53)
_E9RTH = const(0x54)
_E10TTH = const(0x55)
_E10RTH = const(0x56)
_E11TTH = const(0x57)
_E11RTH = const(0x58)
_E12TTH = const(0x59)
_E12RTH = const(0x5a)
_DTR = const(0x5b)
_AFE1 = const(0x5c)
_AFE2 = const(0x5d)
_ECR = const(0x5e)
_CDC0 = const(0x5f)
_CDC1 = const(0x60)
_CDC2 = const(0x62)
_CDC4 = const(0x63)
_CDC5 = const(0x64)
_CDC6 = const(0x65)
_CDC7 = const(0x66)
_CDC8 = const(0x67)
_CDC9 = const(0x68)
_CDC10 = const(0x69)
_CDC11 = const(0x6a)
_CDC12 = const(0x6b)
_CDT_0_1 = const(0x6c)
_CDT_2_3 = const(0x6d)
_CDT_4_5 = const(0x6e)
_CDT_6_7 = const(0x6f)
_CDT_8_9 = const(0x70)
_CDT_10_11 = const(0x71)
_CDT_12 = const(0x72)
_GPIO_CTL0 = const(0x73)
_GPIO_CTL1 = const(0x74)
_GPIO_DIR = const(0x76)
_GPIO_EN = const(0x77)
_GPIO_SET = const(0x78)
_GPIO_CLR = const(0x79)
_GPIO_TOG = const(0x7a)
_AUTO_CONFIG_0 = const(0x7b)
_AUTO_CONFIG_1 = const(0x7c)
_AUTO_CONFIG_USL = const(0x7d)
_AUTO_CONFIG_LSL = const(0x7e)
_AUTO_CONFIG_TL = const(0x7f)


def write(register, value):
    buf = bytearray(2)
    buf[0] = register
    buf[1] = value
    i2c.write(_MAKERBIT_MPR121, buf)


def reset():
    write(0x80, 0x63)


def stop():
    write(_ECR, 0x0)


def start(cl, eleprox, ele):
    write(_ECR, (cl << 6) | (eleprox << 4) | ele)


def read():
    data = i2c.read(_MAKERBIT_MPR121, 2)
    return data[1]<<8 | data[0]


def is_touched(sensor):
    if sensor < 5 or sensor > 16:
        return None
    bit = 0b100000000000 >> (sensor - 5)
    return (bit & read()) != 0


def get_sensor():
    bit = 0b100000000000  # T5
    status = read()
    for sensor in range(5, 17):
        if (bit & status) != 0:
            return sensor  # return first hit
        bit >>= 1
    return None


def init():
    reset()
    stop()

    #
    # Start capturing with default configuration

    # Input filter for rising state
    write(_MHDR, 0x01)
    write(_NHDR, 0x01)
    write(_NCLR, 0x10)
    write(_FDLR, 0x20)

    # Input filter for falling state
    write(_MHDF, 0x01)
    write(_NHDF, 0x01)
    write(_NCLF, 0x10)
    write(_FDLF, 0x20)

    # Input filter for touched state
    write(_NHDT, 0x01)
    write(_NCLT, 0x10)
    write(_FDLT, 0xff)

    # Unused proximity sensor filter
    write(_MHDPROXR, 0x0f)
    write(_NHDPROXR, 0x0f)
    write(_NCLPROXR, 0x00)
    write(_FDLPROXR, 0x00)
    write(_MHDPROXF, 0x01)
    write(_NHDPROXF, 0x01)
    write(_NCLPROXF, 0xff)
    write(_FDLPROXF, 0xff)
    write(_NHDPROXT, 0x00)
    write(_NCLPROXT, 0x00)
    write(_FDLPROXT, 0x00)

    # Debounce configuration (used primarily for interrupts)
    write(_DTR, 0x11)

    # Electrode clock frequency etc
    write(_AFE1, 0xff)
    write(_AFE2, 0x30)

    # Enable autoconfiguration / calibration
    write(_AUTO_CONFIG_0, 0x00)
    write(_AUTO_CONFIG_1, 0x00)

    # Tuning parameters for the autocalibration algorithm
    write(_AUTO_CONFIG_USL, 0x00)
    write(_AUTO_CONFIG_LSL, 0x00)
    write(_AUTO_CONFIG_TL, 0x00)

    # Set touch thresholds
    for i in range(0, 12):
        write(_E0TTH + i * 2, 60)

    # Set release thresholds
    for i in range(0, 12):
        write(_E0RTH + i * 2, 20)

    # Start capture
    start(
        _BaselineTrackingAndInitialize,
        _PROXMITY_DISABLED,
        _TOUCH_ELE_0_TO_11
    )


init()
