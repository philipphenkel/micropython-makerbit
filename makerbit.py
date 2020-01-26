# microbit-module: makerbit@0.0.4

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

from microbit import i2c, pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10, pin11, pin12, pin13, pin14, pin15, pin16
from time import sleep_us, sleep_ms
from time import ticks_us
from machine import time_pulse_us
from micropython import const
from ustruct import unpack

def makerbit_version():
    return "0.0.4"

def _get_pin(pin_index):
    pins = {
        0: pin0,
        1: pin1,
        2: pin2,
        3: pin3,
        4: pin4,
        5: pin5,
        6: pin6,
        7: pin7,
        8: pin8,
        9: pin9,
        10: pin10,
        11: pin11,
        12: pin12,
        13: pin13,
        14: pin14,
        15: pin15,
        16: pin16
    }
    return pins.get(pin_index)


def write_digital_pin(pin_index, value):
    _get_pin(pin_index).write_digital(value)


def write_analog_pin(pin_index, value):
    _get_pin(pin_index).write_analog(value)


def write_led_pins(value):
    for pin_index in range(5, 17):
        _get_pin(pin_index).write_digital(value)


class Motor:
    A = const(0)
    B = const(1)
    FORWARD = const(1)
    BACKWARD = const(-1)

    def __init__(self, motor, rotation=FORWARD):
        if motor == Motor.A:
            self.first_control_pin = pin11
            self.second_control_pin = pin12
            self.speed_pin = pin13
        else:
            self.first_control_pin = pin15
            self.second_control_pin = pin16
            self.speed_pin = pin14
        self.set_rotation(rotation)

    def set_rotation(self, rotation):
        self.rotation = 1 if int(rotation) > 0 else -1

    def stop(self):
        self.first_control_pin.write_digital(0)
        self.second_control_pin.write_digital(0)
        self.speed_pin.write_analog(0)

    def run(self, speed):
        if speed == 0:
            self.stop()
            return

        abs_speed_percentage = min(abs(speed), 100)
        analog_speed = (1023*abs_speed_percentage) // 100

        is_forward = speed * self.rotation > 0
        self.first_control_pin.write_digital(1 if is_forward else 0)
        self.second_control_pin.write_digital(0 if is_forward else 1)
        self.speed_pin.write_analog(analog_speed)


class Ultrasonic:
    DISTANCE_UNIT_CM = const(58)
    DISTANCE_UNIT_INCH = const(148)
    _MAX_ULTRASONIC_TRAVEL_TIME = const(300 * DISTANCE_UNIT_CM)
    _last_trigger_us = 0

    def __init__(self, trig_pin, echo_pin, distance_unit=DISTANCE_UNIT_CM):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.distance_unit = distance_unit

    def get_distance(self):
        # Delay measurement if measure frequency is too high in order to avoid overlapping echos.
        time_to_next_measurement = 3 * Ultrasonic._MAX_ULTRASONIC_TRAVEL_TIME - \
            (ticks_us() - Ultrasonic._last_trigger_us)
        if time_to_next_measurement > 0:
            sleep_us(time_to_next_measurement)

        # Reset pins
        self.echo_pin.read_digital()
        self.trig_pin.write_digital(0)
        sleep_us(2)

        # Trigger sound
        Ultrasonic._last_trigger_us = ticks_us()
        self.trig_pin.write_digital(1)
        sleep_us(10)
        self.trig_pin.write_digital(0)

        # Read echo travel time
        travel_time = time_pulse_us(
            self.echo_pin, 1, Ultrasonic._MAX_ULTRASONIC_TRAVEL_TIME)
        if travel_time <= 0:
            travel_time = Ultrasonic._MAX_ULTRASONIC_TRAVEL_TIME

        # Return distance
        return travel_time // self.distance_unit


class CalibrationLock:
    BaselineTrackingOn = const(0b00)
    BaselineTrackingOff = const(0b01)
    BaselineTrackingAndInitializeFirst5MSB = const(0b10)
    BaselineTrackingAndInitialize = const(0b11)





#class Touch:
    #DISABLED = const(0b0000)
    #ELE_0 = const(0b0001)
    #ELE_0_TO_1 = const(0b0010)
    #ELE_0_TO_2 = const(0b0011)
    #ELE_0_TO_3 = const(0b0100)
    #ELE_0_TO_4 = const(0b0101)
    #ELE_0_TO_5 = const(0b0110)
    #ELE_0_TO_6 = const(0b0111)
    #ELE_0_TO_7 = const(0b1000)
    #ELE_0_TO_8 = const(0b1001)
    #ELE_0_TO_9 = const(0b1010)
    #ELE_0_TO_10 = const(0b1011)
    #ELE_0_TO_11 = const(12) #const(0b1100)

#class Proximity:
#    DISABLED = const(0b00)
#    ELE0_TO_1 = const(0b01)
#    ELE_0_TO_3 = const(0b10)
#    ELE_0_TO_11 = const(0b11)

class Config:
    MHDR = const(0x2b)
    NHDR = const(0x2c)
    NCLR = const(0x2d)
    FDLR = const(0x2e)
    MHDF = const(0x2f)
    NHDF = const(0x30)
    NCLF = const(0x31)
    FDLF = const(0x32)
    NHDT = const(0x33)
    NCLT = const(0x34)
    FDLT = const(0x35)
    MHDPROXR = const(0x36)
    NHDPROXR = const(0x37)
    NCLPROXR = const(0x38)
    FDLPROXR = const(0x39)
    MHDPROXF = const(0x3a)
    NHDPROXF = const(0x3b)
    NCLPROXF = const(0x3c)
    FDLPROXF = const(0x3d)
    NHDPROXT = const(0x3e)
    NCLPROXT = const(0x3f)
    FDLPROXT = const(0x40)
    E0TTH = const(0x41)
    E0RTH = const(0x42)
    E1TTH = const(0x43)
    E1RTH = const(0x44)
    E2TTH = const(0x45)
    E2RTH = const(0x46)
    E3TTH = const(0x47)
    E3RTH = const(0x48)
    E4TTH = const(0x49)
    E4RTH = const(0x4a)
    E5TTH = const(0x4b)
    E5RTH = const(0x4c)
    E6TTH = const(0x4d)
    E6RTH = const(0x4e)
    E7TTH = const(0x4f)
    E7RTH = const(0x50)
    E8TTH = const(0x51)
    E8RTH = const(0x52)
    E9TTH = const(0x53)
    E9RTH = const(0x54)
    E10TTH = const(0x55)
    E10RTH = const(0x56)
    E11TTH = const(0x57)
    E11RTH = const(0x58)
    E12TTH = const(0x59)
    E12RTH = const(0x5a)
    DTR = const(0x5b)
    AFE1 = const(0x5c)
    AFE2 = const(0x5d)
    ECR = const(0x5e)
    CDC0 = const(0x5f)
    CDC1 = const(0x60)
    CDC2 = const(0x62)
    CDC4 = const(0x63)
    CDC5 = const(0x64)
    CDC6 = const(0x65)
    CDC7 = const(0x66)
    CDC8 = const(0x67)
    CDC9 = const(0x68)
    CDC10 = const(0x69)
    CDC11 = const(0x6a)
    CDC12 = const(0x6b)
    CDT_0_1 = const(0x6c)
    CDT_2_3 = const(0x6d)
    CDT_4_5 = const(0x6e)
    CDT_6_7 = const(0x6f)
    CDT_8_9 = const(0x70)
    CDT_10_11 = const(0x71)
    CDT_12 = const(0x72)
    GPIO_CTL0 = const(0x73)
    GPIO_CTL1 = const(0x74)
    GPIO_DIR = const(0x76)
    GPIO_EN = const(0x77)
    GPIO_SET = const(0x78)
    GPIO_CLR = const(0x79)
    GPIO_TOG = const(0x7a)
    AUTO_CONFIG_0 = const(0x7b)
    AUTO_CONFIG_1 = const(0x7c)
    AUTO_CONFIG_USL = const(0x7d)
    AUTO_CONFIG_LSL = const(0x7e)
    AUTO_CONFIG_TL = const(0x7f)


class MPR121:
    def __init__(self, address=0x5A):
        self.address = address
        self.reset()
        self.stop()

        #
        # Start capturing with default configuration

        # Input filter for rising state
        self.set(Config.MHDR, 0x01)
        self.set(Config.NHDR, 0x01)
        self.set(Config.NCLR, 0x10)
        self.set(Config.FDLR, 0x20)

        # Input filter for falling state
        self.set(Config.MHDF, 0x01)
        self.set(Config.NHDF, 0x01)
        self.set(Config.NCLF, 0x10)
        self.set(Config.FDLF, 0x20)

        # Input filter for touched state
        self.set(Config.NHDT, 0x01)
        self.set(Config.NCLT, 0x10)
        self.set(Config.FDLT, 0xff)

        # Unused proximity sensor filter
        self.set(Config.MHDPROXR, 0x0f)
        self.set(Config.NHDPROXR, 0x0f)
        self.set(Config.NCLPROXR, 0x00)
        self.set(Config.FDLPROXR, 0x00)
        self.set(Config.MHDPROXF, 0x01)
        self.set(Config.NHDPROXF, 0x01)
        self.set(Config.NCLPROXF, 0xff)
        self.set(Config.FDLPROXF, 0xff)
        self.set(Config.NHDPROXT, 0x00)
        self.set(Config.NCLPROXT, 0x00)
        self.set(Config.FDLPROXT, 0x00)

        # Debounce configuration (used primarily for interrupts)
        self.set(Config.DTR, 0x11)

        # Electrode clock frequency etc
        self.set(Config.AFE1, 0xff)
        self.set(Config.AFE2, 0x30)

        # Enable autoconfiguration / calibration
        self.set(Config.AUTO_CONFIG_0, 0x00)
        self.set(Config.AUTO_CONFIG_1, 0x00)

        # Tuning parameters for the autocalibration algorithm
        self.set(Config.AUTO_CONFIG_USL, 0x00)
        self.set(Config.AUTO_CONFIG_LSL, 0x00)
        self.set(Config.AUTO_CONFIG_TL, 0x00)

        # Set touch thresholds
        for i in range(0, 12):
            self.set(Config.E0TTH + i * 2, 60)

        # Set release thresholds
        for i in range(0, 12):
            self.set(Config.E0RTH + i * 2, 20)

        # Start capture
        self.start(
            CalibrationLock.BaselineTrackingAndInitialize,
            0b00,    # Proximity.DISABLED,
            0b1100,  # Touch.ELE_0_TO_11
        )

    def set(self, register, value):
        buf = bytearray(2)
        buf[0] = command
        buf[1] = data
        i2c.write(self.address, buf)

    def reset(self):
        self.set(0x80, 0x63)
        sleep_ms(30)

    def stop(self):
        self.set(Config.ECR, 0x0)

    def start(self, cl, eleprox, ele):
        self.set(Config.ECR, (cl << 6) | (eleprox << 4) | ele)

    def readTouchStatus(self):
        res = i2c.read(self.address, 2)
        print(res)
        return unpack("<H", res)[0]

class TouchController:
    def __init__(self):
        self.device = MPR121()

    def isTouched(self):
        res = self.device.readTouchStatus()
        print(res)
        return res
