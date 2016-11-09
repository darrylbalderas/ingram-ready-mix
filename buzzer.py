import os 
import sys
import time 
import math 
from RPi import GPIO


class Buzzer:
  
  def __init__(self,gpioPin, delay, pause,frequency):
    self.buzzerDelay = delay
    self.pauseTime = pause
    self.gpioPin = gpioPin
    self.frequency = frequency 
    
  def stopBuzzer(self):
    print "Function Not Done"
    
  def startBuzzer(self):
    print "Function Not Done"
    
  def getFrequency(self):
    return self.frequency
  
  def setFrequency(self,newFrequency):
    self.frequency = newFrequency 
    
  def getBuzzerDelay(self):
    return self.buzzerDelay
  
  def setBuzzerDelay(self, newBuzzerDelay):
    self.buzzerDelay = newBuzzerDelay
  
  def getPauseTime(self):
    return self.pauseTime
  
  def setPauseTime(self,newPauseTime):
    self.pauseTime = newPauseTime
    
    
