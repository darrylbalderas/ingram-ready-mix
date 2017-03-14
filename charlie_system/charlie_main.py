import sys
import os
from time import sleep
import glob
import serial
from time import time
from charlie_test import *
from transceiver import Transceiver
from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor

if __name__ == "__main__":
  port = xbee_usb_ports()
  if port != None:
    charlie_xbee = Transceiver(9600,port)
    rain_guage = RainGuage(rain_guage_pin, 30)
    flow_sensor = FlowSensor(flow_sensor_pin)
    level_sensor = LevelSensor(level_sensor_pin)

    while True:
      print("Level Sensor state %d" %(level_sensor.check_level_sensor()))
      print("Flow Sensor state %d" %(flow_sensor.check_flow()))
      print("Rain Guage state %d" %(rain_guage.get_tick()))
      print('\n\n')
    #create two threads
    # detect_outfall(xbee,flow_sensor, level_sensor) # thread one
    # detect_rainfall(rain_guage,xbee,level_sensor) # thread two
  else:
    print("Missing xbee device")
