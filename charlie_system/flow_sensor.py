'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the flow sensor.
'''
import RPi.GPIO as gpio


class FlowSensor:
	def __init__(self, pin):
		self.pin = pin

	def check_flow(self):
                '''
                Parameters: None
                Function: Checks whether the gpio pin for flow sensor has
                been invoked resulting in the status either a 1 or 0
                Returns: The status of the flow_sensor
                '''
		return gpio.input(self.pin)

	def check_outfall(self):
                '''
                Parameters: None
                Function: same as check_flow() but this function 
                has a hard 1 or hard zero and there is no flip 
                flopping of the value.  
                Returns: The status of the flow_sensor
                '''
                previous_state = 0
                current_state = self.check_flow()
                if current_state  > previous_state:
                        previous_state = current_state
                        while current_state == previous_state:
                                current_state = self.check_flow()
                        return 1
                else:
                        return 0
