import RPi.GPIO as gpio
import time
import Adafruit_ADS1x15

class LevelSensor:
    def __init__(self):
        self.pool_level = 8.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 1
        self.adc_pin = 0
        self.max_reading = 8
        

    def get_adc_resistance(self, pool_level):
        inches_left = 8.0
        upper_bound = 1130
        lower_bound = 387
        total_boundary = upper_bound - (lower_bound)
        if pool_level > upper_bound:
            pool_level = upper_bound
        elif pool_level < lower_bound:
            pool_level = lower_bound
        tolerance = round((lower_bound/float(total_boundary)) * self.max_reading,2)
        inches_left = round((pool_level/float(total_boundary)) * self.max_reading,2) - tolerance
        if inches_left < 0.2:
            inches_left = 0.0
        return inches_left

    def get_pool_level(self):
        pool_level = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
        #print(pool_level)
        time.sleep(0.25)
        self.pool_level = self.get_adc_resistance(pool_level)
        return self.pool_level

    def check_overflow(self):
        if self.pool_level <= 0.0:
            return 1
        else:
            return 0

def main():
    level = LevelSensor()
    pool_level = 0
    while True:
        pool_level = level.get_pool_level()
        print("The reading of the Level Sensor is: %.2f inches"%(pool_level))
        print("\n")



if __name__ == "__main__":
    main()
