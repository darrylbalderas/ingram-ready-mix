'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the pool level sensor (#eTape Continuous Fluid Level PN 12110215TC-8)
'''
import RPi.GPIO as GPIO
import time 
import numpy as np #Import numpy to send the median on the recorded pool level values
import Adafruit_ADS1x15  #library for ADC hardware

class LevelSensor:
    def __init__(self):
        self.pool_level = 8.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 1
        self.adc_pin = 0
        self.max_voltage_reading = 8
        

    def get_adc_resistance(self, pool_level):
        inches_left = 8.0 
        upper_bound = 1124
        lower_bound = 530
        if pool_level > upper_bound:
            pool_level = upper_bound
        elif pool_level < lower_bound:
            pool_level = lower_bound
        total_boundary = upper_bound - (lower_bound)
        tolerance = round((lower_bound/float(total_boundary))* self.max_voltage_reading,2)
        inches_left = round((pool_level/float(total_boundary)) * self.max_voltage_reading,2) - tolerance
        if inches_left <= 0.2:
            inches_left = 0.0
        return inches_left

    def get_pool_level(self):
        value_list = [ ]
        pool_level = 0.0
        for x in range(3):
                value = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
                time.sleep(0.25)
                value_list.append(value)
        pool_level = np.median(value_list)
        self.pool_level = self.get_adc_resistance(pool_level)
        return self.pool_level

    def check_overflow(self):
        if self.get_pool_level() <= 0.0:
            return 1
        else:
            return 0
