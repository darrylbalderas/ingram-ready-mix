import sys
import os
from time import sleep
import glob
import serial
from time import time
# from transceiver import Transceiver
# from flow_sensor import FlowSensor
# from rain_guage import RainGuage
# from level_sensor import LevelSensor

## gpio pins for the sensors 
##The eTape is a solid state device that measures the fluid levels in water.
#2250 ohms = empty and 400 ohms = full, +-10%

def detect_rain(xbee,rain_guage, level_sensor):
  while True:
    pool_confirmation = ""
    rain_confirmation = ""
    tmp_level = 0 
    rainfall = 0
    floor_level = 0
    ceiling_level = 0
    floor_rating = -0.10
    ceiling_rating = 0.10
    
    if rain_guage.guage_status():
      tmp_level = level_sensor.get_level()
      floor_level = tmp_level + tmp_level*floor_rating
      ceiling_level = tmp_level + tmp_level*ceiling_rating
      #Create the rules here to see the amount of inches needed for outfall
      if ceiling_level == floor_level:
        pool_level = ceiling_level
      else:
        pool_level = ceiling_level - floor_level
      while pool_confirmation != "stop":
        if  rain_guage.get_status():
          rainfall += rain_guage.get_rain()
        pool_confirmation = xbee.receive_message()
        xbee.send_message(str(pool_level)+'\n')

      xbee.clear_serial()
      while rain_guage.status():
        rainfall += rain_guage.get_rain()

      while rain_confirmation != 'stop':
        rain_confirmation = xbee.receive_message()
        xbee.send_message(str(rainfall))
      xbee.clear_serial()

def outfall_detection(flow_sensor,xbee):
  while True:
    outfall_confirmation = ""
    if flow_sensor.get_status():
      while outfall_confirmation != 'stop':
        outfall_confirmation = xbee.receive_message()
        xbee.send_message('out\n')
        

if __name__ == "__main__":
  # rain_guage = RainGuage()
  # flow_sensor = FlowSensor()
  # level_sensor = LevelSensor()
  ##create rainfall_detection thread
  ## pass the rainfall detection function 
  ##create outfall detection thread
  ## pass the outfall detection thread 
  pass
