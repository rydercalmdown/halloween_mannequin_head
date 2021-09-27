import RPi.GPIO as gpio
import time
import logging


class ServoController():

    def __init__(self):
        """Set up the servos"""
        logging.info('Setting up servo')
        self.servo_pin = 3
        self._setup_gpio()
        self._set_servo_range()

    def _set_servo_range(self):
        """Sets the range of the servo"""
        self.servo_bounds_degrees = 20
        self.servo_max = 180 - self.servo_bounds_degrees
        self.servo_min = self.servo_bounds_degrees
        self.servo_range = self.servo_max - self.servo_min

    def __del__(self):
        """Clean up"""
        self.pwm.stop()
        gpio.cleanup()

    def _setup_gpio(self):
        """Set up the gpio"""
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.servo_pin, gpio.OUT)
        self.pwm = gpio.PWM(self.servo_pin, 50)
        self.pwm.start(0)

    def set_servo_angle(self, angle):
        """Set the angle of the servo"""
        logging.info('Setting angle to {}'.format(angle))
        gpio.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(angle / 18 + 2)
        time.sleep(1)
        gpio.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)

    def set_servo_percent(self, percent):
        """Converts a decimal percentage into servo angle"""
        angle = int((1 - percent) * self.servo_range) + self.servo_min
        self.set_servo_angle(angle)
