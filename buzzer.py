import os 
import sys
import time 
from RPi import GPIO

class Buzzer:
  
  def __init__(self,gpioPin, delay, pause):
    self.buzzer_delay = delay
    self.pause_time = pause
    self.gpioPin = gpioPin
    
  def stopBuzzer(self):
    print "Function Not Done"
    
  def startBuzzer(self):
    print "Function Not Done"
    
print "hello"
