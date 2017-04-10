'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This program was written to test buzzers soldered on pcd board. Uses
user input to (Y) invoke the buzzers or (N) to exit the program

5 Volts DC - Pin 2 or Pin 4
3.3 Volts DC -  Pin 1
Ground - Pin 6 

Check website for more pin layout:
http://blog.mcmelectronics.com/post/Raspberry-Pi-3-GPIO-Pin-Layout
'''

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD) 
buzzers = [7,11,13,15,29,31,33,35]

def initalize_buzzers(buzzers):
  '''
  Parameters: None
  Function: Initializes the pins used by the buzzers as output
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.setup(buzzer,gpio.OUT)

def start_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending
  a boolean value True in order to turn on
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.output(buzzer,True)

def stop_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending 
  a boolean value False in order to turn off
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.output(buzzer,False)


def main():
    initalize_buzzers(buzzers)
    while True:
          try:
            user_input = raw_input("Enter (Y) to turn on buzzers or (N) to exit program: ")
            if user_input.lower() == "y":
              print("Buzzing for 3 seconds")
              start_buzzer()
              sleep(3)
              stop_buzzer()
            elif user_input.lower() == 'n':
              print('Exiting program')
              break
          except KeyboardInterrupt:
            print("\nExiting program")


if __name__ == "__main__":
  main()
