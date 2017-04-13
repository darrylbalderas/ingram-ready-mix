'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the Rain guage sensor 
'''

import os
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
		collection_duration = 3
		while (time()-previous_time) <= collection_duration:
			current_state = self.check_guage()
			if current_state  > previous_state:
			    previous_state = current_state
			    while current_state == previous_state:
			        current_state = self.check_guage()
			    return 1
		return 0
              
	def get_total_rainfall(self,restart_pin,restart_hold, level_sensor):
		'''
		Parameters: restart_pin(integer), restart_hold(integer)
		Function: Collects the number of rainfall until the max collection time 
		has been reached or rain_guage stop ticking. 
		Returns: The amount of rainfall
		'''
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
				restart_state(restart_pin, restart_hold, level_sensor, rainfall)

		return rainfall


RAIN = './config_files/rain_val.txt'
POOL_LEVEL = './config_files/pool_level.txt'
RESTART = './config_files/restart.txt'
RAINING = './config_files/raining.txt'


def restart_state(restart_pin, restart_hold, level_sensor, rainfall):
  '''
  Paramter: restart_pin(integer), restart_hold(integer)
  Function: If the user has succesfully hold the restart
  button for 3 seconds then the system will restart otherwise it break 
  from this function.
  Returns: None
  '''
  state  = 0
  end_time = 0
  start_time = time()
  while end_time < restart_hold:
    end_time = time() - start_time
    state = gpio.input(restart_pin)
    if not state:
      return
  str_rainfall = str(rainfall)
  str_pool_level = str(level_sensor.get_pool_level())
  set_value_file(RAIN,str_rainfall)
  set_value_file(POOL_LEVEL,str_pool_level)
  set_value_file(RESTART, '1')
  set_value_file(RAINING,'1')
  os.system("sudo reboot")

def set_value_file(file_name, value):
  if os.path.exists(file_name):
    fopen = open(file_name,'w')
    fopen.write(value)
    fopen.close()
  else:
    return None

