# microbit-module: makerbit@0.0.3
from microbit import pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10, pin11, pin12, pin13, pin14, pin15, pin16
from time import sleep_us
from time import ticks_us
from machine import time_pulse_us
from micropython import const


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
