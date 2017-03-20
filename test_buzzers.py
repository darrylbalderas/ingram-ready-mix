import RPi.GPIO as gpio
from time import sleep

buzzers = [4,17,22,27,5,6,13,19] ## wiring in beardboard

def initalize_buzzers(buzzers):
  for buzzer in buzzers:
    gpio.setup(buzzer,gpio.OUT)

def start_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,True)

def stop_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,False)


def main():
	initalize_buzzers(buzzers)
	while True:
		input_value = raw_input("Enter a key: (Turn on buzzers (Y or y)")
		if input_value.lower() == "y":
			print("Buzzing for three seconds")
			start_buzzer()
			sleep(3)
			stop_buzzer()
