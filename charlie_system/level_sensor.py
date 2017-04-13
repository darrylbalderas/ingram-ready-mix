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
        self.pool_level = 12.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 1
        self.adc_pin = 0
        

    def get_adc_resistance(self, pool_level):
        inches_left = 12.0 
        upper_bound = 1100
        lower_bound = 350
        total_boundary = upper_bound - (lower_bound)
        tolerance = round((pool_level/float(total_boundary))* 12,2)
        inches_left = round((pool_level/float(total_boundary)) * 12,2) - tolerance
        return inches_left

    def get_pool_level(self):
        value_list = [ ]
        pool_level = 0
        for x in range(5):
                value = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
                value_list.append(value)
                time.sleep(0.5)
        pool_level = np.median(value_list)
        self.pool_level = self.get_adc_resistance(pool_level)
        return self.pool_level

    def check_overflow(self):
        if self.pool_level  < 0.5:
            return 1
        else:
            return 0
