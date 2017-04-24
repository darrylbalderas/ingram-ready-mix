'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the Rain guage sensor 
'''

# import os
import RPi.GPIO as gpio
from time import time

class RainGuage:
	def __init__(self,pin,time_interval):
		self.pin = pin
		self.max_time = time_interval * 60

	def check_guage(self):
		'''
		Parameters: None
		Function: Checks whether the gpio pin for check_guage has
		been invoked resulting in the status either a 1 or 0
		Returns: The status of the rain_guage
		'''
		return gpio.input(self.pin)

	def get_tick(self):
		'''
		Parameters: None
		Function: Checks whether the rain guage has been triggered. It
		has a 3 second timeout. 
		Returns: The status of the rain_guage
		'''
		previous_state = 0
		previous_time = time()
		collection_duration = 2.0
		while (time()-previous_time) <= collection_duration:
			current_state = self.check_guage()
			if current_state  > previous_state:
			    previous_state = current_state
			    while current_state == previous_state:
			        current_state = self.check_guage()
			    return 1
		return 0
              
	def get_total_rainfall(self):
		'''
		Parameters: restart_pin(integer), restart_hold(integer)
		Function: Collects the number of rainfall until the max collection time 
		has been reached or rain_guage stop ticking. 
		Returns: The amount of rainfall
		'''
		rainfall = 0.011
		previous_time = time()
		while (time()-previous_time) <= self.max_time:
			if not self.get_tick():
				break
			else:
				rainfall += 0.011
		return rainfall
