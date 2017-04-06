import glob 
import sys
from time import sleep
import os
import RPi.GPIO as gpio
from time import time

class RainGuage:
	def __init__(self,pin,time_interval):
		self.pin = pin
		self.max_time = time_interval * 60

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
		while (time()-previous_time) <= self.max_time:
			ticking = self.get_tick()
			if not ticking:
				break
			else:
				rainfall += 0.1690

			if gpio.input(restart_pin):
				restart_state(restart_pin, restart_hold)

		return rainfall


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

