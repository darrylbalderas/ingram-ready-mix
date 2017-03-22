import RPi.GPIO as gpio
from time import sleep

flow = 23
level = 24
rain = 18
max_time = 30 * 60
gpio.setmode(gpio.BCM)
gpio.setup(flow,gpio.IN)
gpio.setup(level,gpio.IN)
gpio.setup(rain,gpio.IN)

def check_rainguage():
  return gpio.input(rain)

def check_flowsensor():
  return gpio.input(flow)

def check_levelsensor():
  return gpio.input(level)

def check_buttons():
  while True:
    print("This is the value for rainguage button: %d" %(check_rainguage()))
    print("This is the value for flow sensor button: %d" %(check_flowsensor()))
    print("This is the value for level sensor button: %d" %(check_levelsensor()))
    print('\n\n')
    sleep(0.5)

if __name__ == "__main__":
	check_buttons()


