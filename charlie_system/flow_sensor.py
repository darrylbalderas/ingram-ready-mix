import sys
from time import sleep
import RPi.GPIO as gpio
from time import time


class FlowSensor:
	def __init__(self, pin):
		self.pin = pin

	def check_flow(self):
		return gpio.input(self.pin)

	def check_outfall(self):
                previous_state = 0
                current_state = self.check_flow()
                if current_state  > previous_state:
                        previous_state = current_state
                        while current_state == previous_state:
                                current_state = self.check_flow()
                        return 1
                else:
                        return 0
