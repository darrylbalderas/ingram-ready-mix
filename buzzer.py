import os 
import sys
import time 
import math 
import RPi.GPIO as gpio

class Buzzer:
  
  def __init__(self, gpio_pin, board_type):
    self.__buzzer_pin = gpio_pin

    if board_type.lower() == "bcm":
      gpio.setmode(gpio.BCM)
    elif board_type.lower() == "board":
      gpio.setmode(gpio.BOARD)
    gpio.setup(self.__buzzer_pin, gpio.OUT)
    
  def stop(self):
    gpio.output(self.__buzzer_pin,False)
    
  def start(self):
    gpio.output(self.__buzzer_pin,True)

  def set_pin(self, gpio_pin):
    self.__buzzer_pin = gpio_pin

  def get_pin(self):
    return self.__buzzer_pin
  


    
    
