import glob 
import sys
from time import sleep
import RPi.GPIO as GPIO

class RainGuage:
	def __init__(self,pin,time_interval):
		self.pin = pin
		self.max_time = time_interval * 60

	def check_guage(self):
		return GPIO.input(self.pin)

	def get_tick(self):
		previous = 0
		current_state = self.check_guage()
		if current_state > previous:
			previous = current_state
		    while current_state == previous:
		      current_state = self.check_guage()
		    previous = 0
		    return True
		else:
			return False

	def get_total_rainfall(self):
		previous = time()
		rainfall = 0
		while (time()-previous) <= self.max_time:
			if get_tick():
				rainfall += 0.011
		return rain

