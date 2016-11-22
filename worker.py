import sys
import os 
import alarmSystem 
import time 
import Buzzer
import math 

class Worker:
  
  name = "Ingram Employee"
  def __init__(self, alarmSystem,buzzer):
    self.alarmsystem = alarmSystem
    self.start_time = 0
    self.end_time = 0
    self.buzzer = buzzer
   
  def start_AlarmSystem(self, gpioPins):
    print "Function Not Done"
    
  def stop_AlarmSystem(self, gpioPins):
    print "Function Not Done
    
  def sample_collected(self, gpioPins):
    print "Function Not Done"
    
  def sample_missed(self,gpioPins):
    print "Function Not Done"
    
  def restart_System(self,gpioPins):
    print "Function Not Done"
    
  def get_startTime(self):
    return self.start_time
  
  def set_startTime(self,new_time):
    self.start_time = new_time
    
  def get_endTime(self):
    return self.start_time
  
  def set_endTime(self,new_time):
    self.end_time = new_time
