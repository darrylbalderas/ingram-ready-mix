import RPi.GPIO as GPIO
import time
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
        pool_level = self.adc.read_adc(0, gain=self.GAIN)
        time.sleep(0.5)
        self.pool_level = self.get_adc_resistance(pool_level)
        return self.pool_level

    def check_overflow(self):
        if self.pool_level == 0.0:
            return 1
        else:
            return 0


def main():
    level = LevelSensor()
    pool_level = 0
    while True:
        pool_level = level.get_pool_level()
        print("The reading of the Level Sensor is: %f inches"%(pool_level))
        print("\n")



if __name__ == "__main__":
    main()