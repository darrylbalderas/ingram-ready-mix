import RPi.GPIO as gpio
from time import sleep

complete = 12 
mute = 20
miss = 16
restart = 21
gpio.setmode(gpio.BCM)
gpio.setup(complete,gpio.IN)
gpio.setup(mute,gpio.IN)
gpio.setup(miss,gpio.IN)
gpio.setup(restart,gpio.IN)

def check_complete():
  return gpio.input(complete)

def check_miss():
  return gpio.input(miss)

def check_mute():
  return gpio.input(mute)

def check_restart():
  return gpio.input(restart)

def check_buttons():
  while True:
    print("This is the value for complete button: %d" %(check_complete()))
    print("This is the value for missed button: %d" %(check_miss()))
    print("This is the value for mute button: %d" %(check_mute()))
    print("This is the value for restart button: %d" %(check_restart()))
    print('\n\n')
    sleep(1.0)

if __name__ == "__main__":
	check_buttons()


