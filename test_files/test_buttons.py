'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This program was written to test buttons soldered on pcd board. Loops 
contiuously to check the status of the buttons. Press Ctrl + C to exit program.

5 Volts DC - Pin 2 or Pin 4
3.3 Volts DC -  Pin 1
Ground - Pin 6 

Check website for more pin layout:
http://blog.mcmelectronics.com/post/Raspberry-Pi-3-GPIO-Pin-Layout
'''

import RPi.GPIO as gpio
from time import sleep

complete = 32
mute = 36
miss = 38
restart = 40
gpio.setmode(gpio.BOARD)
gpio.setup(complete,gpio.IN)
gpio.setup(mute,gpio.IN)
gpio.setup(miss,gpio.IN)
gpio.setup(restart,gpio.IN)


def check_complete():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for complete button has
  been pressed resulting in the status either a 1 or 0
  Returns: The status of the complete button
  '''
  return gpio.input(complete)

def check_miss():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for miss button has been 
  pressed resulting in the status either a 1 or 0
  Returns: The status of the missed button
  '''
  return gpio.input(miss)

def check_mute():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for mute button has been
  pressed resulting in the status either a 1 or 0
  Returns: The status of the mute button
  '''
  return gpio.input(mute)

def check_restart():
  '''
  Parameter: None
  Function: Checks whether the gpio pin for restart button has been
  pressed resulting in the status either a 1 or 0
  Returns: The status of the restart button
  '''
  return gpio.input(restart)

def check_buttons():
  while True:
    try:
      print("This is the value for complete button: %d" %(check_complete()))
      print("This is the value for missed button: %d" %(check_miss()))
      print("This is the value for mute button: %d" %(check_mute()))
      print("This is the value for restart button: %d" %(check_restart()))
      print('\n\n')
      sleep(0.5)
    except KeyboardInterrupt:
      print("Exiting Program")

if __name__ == "__main__":
	check_buttons()


