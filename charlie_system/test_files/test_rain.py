import os
import RPi.GPIO as gpio
from time import time

class RainGuage:
    def __init__(self,pin,time_interval):
        self.pin = pin
        self.max_time = time_interval * 60
        gpio.setup(self.pin,gpio.IN)

    def check_guage(self):
        return gpio.input(self.pin)

    def get_tick(self):
        previous_state = 0
        previous_time = time()
        collection_duration = 1.5
        while (time()-previous_time) <= collection_duration:
            current_state = self.check_guage()
            if current_state  > previous_state:
                previous_state = current_state
                while current_state == previous_state:
                    current_state = self.check_guage()
                return 1
        return 0
              
    def get_total_rainfall(self):
        rainfall = 0.011
        ticking = 0
        previous_time = time()
        num_ticks = 1
        while (time()-previous_time) <= self.max_time:
            ticking = self.get_tick()
            if not ticking:
                break
            else:
                rainfall += 0.011
                num_ticks += 1

        return (rainfall,num_ticks)




def main():
        gpio.setmode(gpio.BOARD)
        rain_guage_pin = 12
        rain_collection_time = 30 #minutes
        rain_guage = RainGuage(rain_guage_pin,rain_collection_time)
        while True:
                rainfall = 0
                num_ticks = 0
                if rain_guage.get_tick():
                        rainfall,num_ticks = rain_guage.get_total_rainfall()
                        print("%.3f inches of rainfall and %d number of ticks collected from rain guage"%(rainfall,num_ticks))

if __name__ == "__main__":
    main()

