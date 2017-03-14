import glob 
import sys
from time import sleep
import RPi.GPIO as GPIO
from time import time

class RainGuage:
	def __init__(self,pin,time_interval):
		self.pin = pin
		self.max_time = time_interval * 60

	def check_guage(self):
		return GPIO.input(self.pin)

	def get_tick(self):
		previous_state = 0
		previous_time = 0
		collection_duration = 2
		while (time()-previous_time) <= collection_duration:
			current_state = self.check_guage()
			if current_state > previous_state:
				previous_state = current_state
				while current_state == previous_state:
					current_state = self.check_guage()
				previous_state = 0
				return True
		return False

	def get_total_rainfall(self):
		rainfall = 0.011
		ticking = False
		previous_time = time()
		while (time()-previous_time) <= self.max_time:
			ticking = self.get_tick()
			if not ticking:
				break
			else:
				rainfall += 0.011
		return rainfall

