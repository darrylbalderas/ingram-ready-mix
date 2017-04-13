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
        self.voltage_level = 12.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 2
        self.adc_pin = 1

    def get_adc_voltage(self, voltage_level):
        voltage_reading = 12.0 # default voltage level
        upper_bound = 1390
        lower_bound = 0
        total_boundary = upper_bound - (lower_bound)
        if voltage_level < 0:
            voltage_level = 0.0
        tolerance = round((voltage_level/float(total_boundary))* 14, 2)
        voltage_reading = round((voltage_level/float(total_boundary))*14, 2) - tolerance
        return voltage_reading

    def get_voltage_level(self):
        value_list = [ ]
        voltage_level = 0
        for x in range(5):
                value = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
                value_list.append(value)
                time.sleep(0.5)
        voltage_level = np.median(value_list)
        self.voltage_level = self.get_adc_voltage(voltage_level)
        return self.voltage_level

