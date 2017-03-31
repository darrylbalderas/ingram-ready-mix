import RPi.GPIO as GPIO

import time

#Import numpy to send the median on the recorded pool level values
import numpy as np

#Import the ADS1x15 module.
import Adafruit_ADS1x15



class Battery:
    def __init__(self):
        self.voltage_level = 12
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1

    def get_resistance_voltageLevel(self, voltage_level):
        voltage_reading = 12
        if voltage_level >= 15000 and voltage_level <= 157000:
            voltage_reading = 12
        elif voltage_level >= 14300 and voltage_level <= 14999:
            voltage_reading = 11
        elif voltage_level >= 13300 and voltage_level <= 14299:
            voltage_reading = 10
        elif voltage_level >= 12200 and voltage_level <= 13299:
            voltage_reading = 9
        elif voltage_level >= 11100 and voltage_level <= 12199:
            voltage_reading = 8
        elif voltage_level >= 9000 and voltage_level <= 11099:
            voltage_reading = 7
        elif voltage_level >= 7600 and voltage_level <= 8999:
            voltage_reading = 6
        elif voltage_level >= 4000 and voltage_level <= 7599:
            voltage_reading = 5

        return voltage_reading

    def get_voltage_level(self):
        num_list = []
        voltage_level = 0
        for x in xrange(30):
                value = self.adc.read_adc_difference(0, gain=self.GAIN)
                num_list.append(value)
                time.sleep(0.5)
        voltage_level = np.median(num_list)
        self.voltage_level = self.get_resistance_voltageLevel(voltage_level)
        return self.voltage_level

    def check_status(self):
        if self.voltage_level < 6:
            return 1
        else:
            return 0
