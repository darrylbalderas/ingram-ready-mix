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
        collection_duration = 3
        while (time()-previous_time) <= collection_duration:
            current_state = self.check_guage()
            if current_state  > previous_state:
                previous_state = current_state
                while current_state == previous_state:
                    current_state = self.check_guage()
                return 1
        return 0
              
    def get_total_rainfall(self,restart_pin,restart_hold):
        rainfall = 0.1690
        ticking = 0
        previous_time = time()
        num_ticks = 1
        while (time()-previous_time) <= self.max_time:
            ticking = self.get_tick()
            if not ticking:
                break
            else:
                rainfall += 0.1690
                num_ticks += 1

            if gpio.input(restart_pin):
                restart_state(restart_pin, restart_hold)

        return (rainfall,num_ticks)


def restart_state(restart_pin,restart_hold):
  state  = 0
  end_time = 0
  start_time = time()
  while end_time < restart_hold:
    end_time = time() - start_time
    state = gpio.input(restart_pin)
    if not state:
      return
  os.system("sudo reboot")


def main():
        gpio.setmode(gpio.BOARD)
        rain_guage_pin = 12
        restart_button_pin = 8 
        rain_collection_time = 30 #minutes
        restart_button_hold = 3  # seconds
        gpio.setup(restart_button_pin,gpio.OUT)
        rain_guage = RainGuage(rain_guage_pin,rain_collection_time)
        while True:
                rainfall = 0
                num_ticks = 0
                if rain_guage.get_tick():
                        rainfall,num_ticks = rain_guage.get_total_rainfall(restart_button_pin, restart_button_hold)
                        print("%f inches of rainfall and %d number of ticks collected from rain guage"%(rainfall,num_ticks))

if __name__ == "__main__":
    main()

