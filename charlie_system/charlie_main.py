import sys
import os
from time import sleep
import glob
import serial
from time import time
import RPi.GPIO as GPIO
from transceiver import Transceiver
# from transceiver import Transceiver
# from flow_sensor import FlowSensor
# from rain_guage import RainGuage
# from level_sensor import LevelSensor

#initialize the GPIO pins for the sensors
rain_guage = 8
level_sensor = 16
flow_sensor = 10
GPIO.setmode(GPIO.BOARD)
GPIO.setup(flow_sensor,GPIO.IN)
GPIO.setup(level_sensor,GPIO.IN)
GPIO.setup(rain_guage,GPIO.IN)
charlie_xbee = Transceiver()


def check_guage():
  return GPIO.input(rain_guage)

def check_flow():
  return GPIO.input(flow_sensor)

def check_level_sensor():
  return GPIO.input(level_sensor)

def detect_outfall():
  

def check_tick(current_state):
  previous = 0
  if current_state > previous:
    previous = current_state
    while current_state == previous:
      current_state = check_guage()
    previous = 0
    return True
  else:
    return False
  

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
    
    #eTape Continuous Fluid Level PN-12110215TC-12
    #Sensor Output: 2250ohms empty, 400 ohms full +- 10%
    if rain_guage.guage_status():
      tmp_level = level_sensor.get_level()
      floor_level = tmp_level + tmp_level*floor_rating
      ceiling_level = tmp_level + tmp_level*ceiling_rating
      
    #Create the rules here to see the amount of inches needed for outfall
    #pool_level equals the amount left for outfall to occur

    if floor_level >= 2190 & ceiling_level <= 2200:     #Between 0 to 1 inches filled on tape
      pool_level = 12
    elif floor_level >= 2020 & ceiling_level <= 2189:   #Between 1 to 2 inches filled on tape
      pool_level = 11
    elif floor_level >= 1890 & ceiling_level <= 2019:   #Between 2 to 3 inches filled on tape
      pool_level = 10
    elif floor_level >= 1710 & ceiling_level <= 1889:   #Between 3 to 4 inches filled on tape
      pool_level = 9
    elif floor_level >= 1550 & ceiling_level <= 1709:   #Between 4 to 5 inches filled on tape
      pool_level = 8
    elif floor_level >= 1390 & ceiling_level <= 1549:   #Between 5 to 6 inches filled on tape
      pool_level = 7
    elif floor_level >= 1220 & ceiling_level <= 1389:   #Between 6 to 7 inches filled on tape
      pool_level = 6
    elif floor_level >= 1080 & ceiling_level <= 1219:   #Between 7 to 8 inches filled on tape
      pool_level = 5
    elif floor_level >= 910 & ceiling_level <= 1079:    #Between 8 to 9 inches filled on tape
      pool_level = 4
    elif floor_level >= 770 & ceiling_level <= 909:     #Between 9 to 10 inches filled on tape
      pool_level = 3
    elif floor_level >= 610 & ceiling_level <= 769:     #Between 10 to 11 inches filled on tape
      pool_level = 2
    elif floor_level >= 420 & ceiling_level <= 609:     #Between 11 to 12 inches filled on taped
      pool_level = 1
    elif floor_level >= 380 & ceiling_level <= 419:
      pool_level = 0
    else:
      pass
      
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
