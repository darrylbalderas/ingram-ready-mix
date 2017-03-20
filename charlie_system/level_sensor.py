import RPi.GPIO as GPIO

import time

#Import numpy to send the median on the recorded pool level values
import numpy as np

# Import the ADS1x15 module.
import Adafruit_ADS1x15



class LevelSensor:
    def __init__(self):
        self.pool_level = 8
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        

    def resistance_to_inches(self, pool_level):
        inches_left = 8
        
        if pool_level >= 15000 and pool_level <= 157000: #Between 0 to 1 inches filled on tap
            inches_left = 7
        elif pool_level >= 14300 and pool_level <= 14999: #Between 1 to 2 inches filled on tape
            inches_left = 6
        elif pool_level >= 13300 and pool_level <= 14299: #Between 2 to 3 inches filled on tape
            inches_left = 5
        elif pool_level >= 12200 and pool_level <= 13299: #Between 3 to 4 inches filled on tape
            inches_left = 4
        elif pool_level >= 11100 and pool_level <= 12199: #Between 4 to 5 inches filled on tape
            inches_left = 3
        elif pool_level >= 9000 and pool_level <= 11099: #Between 5 to 6 inches filled on tape
            inches_left = 2
        elif pool_level >= 7600 and pool_level <= 8999: #Between 6 to 7 inches filled on tape
            inches_left = 1
        elif pool_level >= 4000 and pool_level <= 7599: #Between 7 to 8 inches filled on tape
            inches_left = 0

        return inches_left

    def get_pool_level(self):
        #eTape Continuous Fluid Level PN 12110215TC-8
        num_list = []
        pool_level = 0
        for x in xrange(30):
                value = self.adc.read_adc_difference(0, gain=self.GAIN)
                num_list.append(value)
                time.sleep(0.5)
        pool_level = np.median(num_list)
        self.pool_level = self.resistance_to_inches(pool_level)
          
        #Create the rules here to see the amount of inches needed for outfall
        #pool_level equals the amount left for outfall to occur
        return self.pool_level

    def check_overflow(self):
        if self.pool_level == 0:
            return 1
        else:
            return 0

def main():
        level = LevelSensor()
        print(level.get_pool_level())

main()





