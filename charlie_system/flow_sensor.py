import RPi.GPIO as GPIO

class FlowSensor:
	def __init__(self, pin):
		self.pin = pin

	def check_flow(self):
		return GPIO.input(self.pin)

	def check_outfall(self):
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
