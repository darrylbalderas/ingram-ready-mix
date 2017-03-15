# import sys
# import os
# from time import sleep
# import glob
# import serial
# from time import time
# from charlie_test import *
# from transceiver import Transceiver
# from flow_sensor import FlowSensor
# from rain_guage import RainGuage
# from level_sensor import LevelSensor

# if __name__ == "__main__":
#   port = xbee_usb_port()
#   if port != None:
#     charlie_xbee = Transceiver(9600,port)
#     rain_guage = RainGuage(rain_guage_pin,30)
#     flow_sensor = FlowSensor(flow_sensor_pin)
#     level_sensor = LevelSensor(level_sensor_pin) 
#     #create two threads
#     detect_outfall(xbee,flow_sensor, level_sensor) # thread one
#     detect_rainfall(rain_guage,charlie_xbee,level_sensor) # thread two
#   else:
#     print("Missing xbee device")


from threading import Thread
from time import sleep
from threading import Lock

def threaded_function(arg,lock):
  while True:
    lock.acquire()
    message = raw_input("Enter a value for thread 1: ")
    if message == 'n':
      lock.release()
      break
    else:
      print("wrong input for thread 1")
    lock.release()


def say_something(arg,lock):
  while True:
    lock.acquire()
    message = raw_input("Enter a value for thread 2: ")
    if message == 'n':
      lock.release()
      break
    else:
      print("wrong input for thread 2")
    lock.release()


if __name__ == "__main__":
  lock = Lock()
  thread = Thread(target = threaded_function, args = (5,lock,))
  thread2 = Thread(target = say_something, args = (5,lock,))
  thread.start()
  thread2.start()
  thread.join()
  thread2.join()
  print "thread finished...exiting"

