import sys
import os
from time import sleep
import glob
import serial
from time import time
# from charlie_test import *
# from transceiver import Transceiver
# from flow_sensor import FlowSensor
# from rain_guage import RainGuage
# from level_sensor import LevelSensor
from threading import Thread
from threading import Lock
from threading import Event

if __name__ == "__main__":
  lock = Lock()
  event = Event()
  port = xbee_usb_port()
  if port != None:
    try:
      charlie_xbee = Transceiver(9600,port)
      rain_guage = RainGuage(rain_guage_pin,30)
      flow_sensor = FlowSensor(flow_sensor_pin)
      level_sensor = LevelSensor(level_sensor_pin) 
      detect_outfall(charlie_xbee,flow_sensor, level_sensor) 
      detect_rainfall(rain_guage,charlie_xbee,level_sensor) 
      thread1 = Thread(target = detect_outfall, args = (charlie_xbee,flow_sensor,level_sensor,lock,event, ))
      thread2 = Thread(target = detect_rainfall, args = (rain_guage, charlie_xbee, level_sensor,lock,event,))
      thread1.start()
      thread2.start()
    except KeyboardInterrupt:
      event.set()
      print("Ending the program")
      thread1.join()
      thread2.join()
      
  else:
    print("Missing xbee device")
