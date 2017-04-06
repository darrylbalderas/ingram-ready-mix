import RPi.GPIO as GPIO
import time
#Import numpy to send the median on the recorded pool level values
import numpy as np
# Import the ADS1x15 module.
import Adafruit_ADS1x15

class LevelSensor:
    def __init__(self):
        self.pool_level = 12.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 1
        

    def get_adc_resistance(self, pool_level):
        inches_left = 12.0
        upper_bound = 1110
        lower_bound = 350
        total_boundary = upper_bound - (lower_bound)
        inches_left = round((pool_level/float(total_boundary)) * 12,2)
        return inches_left

    def get_pool_level(self):
        #eTape Continuous Fluid Level PN 12110215TC-8
        value_list = []
        pool_level = 0
        for x in range(5):
                value = self.adc.read_adc(0, gain=self.GAIN)
                value_list.append(value)
                time.sleep(0.5)
        pool_level = np.median(value_list)
        self.pool_level = self.get_adc_resistance(pool_level)
          
        #Create the rules here to see the amount of inches needed for outfall
        #pool_level equals the amount left for outfall to occur
        return self.pool_level

    def check_overflow(self):
        if self.pool_level == 0.0:
            return 1
        else:
            return 0
