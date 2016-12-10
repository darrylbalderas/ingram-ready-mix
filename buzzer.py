import os 
import sys
import time 
import math 
from RPi import GPIO

class Buzzer:
  
  def __init__(self, gpio_pin):
    self.__buzzer_pin = gpio_pin
    self.__frequencies = [261, 294, 329, 349, 392, 440, 493, 423]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.__buzzer_pin, GPIO.OUT)
    
    
  def stop_buzzer(self):
    GPIO.output(self.__buzzer_pin,False)
    
    
  def start_buzzer(self):
    GPIO.output(self.__buzzer_pin,True)
    
    
  def get_frequencies(self):
    return self.__frequencies
  
  def set_frequencies(self,new_frequency):
    self.__frequencies = new_frequency 
    
def main():
   
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(12, GPIO.OUT)
  p = GPIO.PWM(12, 100)  
  p.start(100)
  




if __name__ == '__main__':
  main()

    
    
    
