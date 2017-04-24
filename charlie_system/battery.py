'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality needt to access the battery
'''
import RPi.GPIO as GPIO
import time
import numpy as np
import Adafruit_ADS1x15 #library for ADC hardware
 
class Battery:
    def __init__(self):
        self.voltage_level = 13.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 2
        self.adc_pin = 1
        self.max_voltage_reading = 14

    def get_adc_voltage(self, voltage_level):
        voltage_reading = 13.0 #default voltage level
        upper_bound = 1367
        lower_bound = 0
        if voltage_level < lower_bound:
            voltage_level = lower_bound
        elif voltage_level > upper_bound:
            voltage_level = upper_bound
        total_boundary = upper_bound - (lower_bound)
        tolerance = round((lower_bound/float(total_boundary)) * self.max_voltage_reading, 2)
        voltage_reading = round((voltage_level/float(total_boundary)) * self.max_voltage_reading, 2) - tolerance
        return voltage_reading

    def get_voltage_level(self):
        voltage_level = 0
        value = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
        time.sleep(0.25)
        voltage_level = np.median(value)
        self.voltage_level = self.get_adc_voltage(voltage_level)
        return self.voltage_level

