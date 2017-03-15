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
from threading import Thread
from threading import Lock

if __name__ == "__main__":
  lock = Lock()
  port = xbee_usb_port()
  if port != None:
    charlie_xbee = Transceiver(9600,port)
    rain_guage = RainGuage(rain_guage_pin,30)
    flow_sensor = FlowSensor(flow_sensor_pin)
    level_sensor = LevelSensor(level_sensor_pin) 
    detect_outfall(charlie_xbee,flow_sensor, level_sensor) # thread one
    detect_rainfall(rain_guage,charlie_xbee,level_sensor) # thread two
    thread1 = Thread(target = detect_outfall, args = (charlie_xbee,flow_sensor,level_sensor,lock, ))
    thread2 = Thread(target = detect_rainfall, args = (rain_guage, charlie_xbee, level_sensor,lock,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
  else:
    print("Missing xbee device")

