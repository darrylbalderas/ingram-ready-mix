import sys
import os
from time import sleep
import glob
import serial
from time import time
from threading import Thread
from threading import Lock
from threading import Event
##import RPi.GPIO as gpio
from transceiver import Transceiver
import datetime
from multiprocessing import Process
import Queue
import random

# class Job(object):
#     def __init__(self, priority, message):
#         self.priority = priority
#         self.description = message
#     def __cmp__(self, other):
#         return cmp(self.priority,other.priority)

def remove_character(message,character):
  return message.strip(character)

def xbee_usb_port():
  if sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
  elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')

  if len(ports) != 0:
      result = []
      for port in ports:
          try:
              ser = serial.Serial(port)
              ser.close()
              result.append(port)
          except( OSError, serial.SerialException):
              pass
      return result[0]
  else:
      return None

def send_confirmation(receive_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while not receive_queue.empty():
      sleep(random.random())
      message = receive_queue.get()
      print("inside send_confirmation")
      print(message)
      receive_queue.task_done()
      if message == "tri":
        print("received trigger")
        for x in range(4):
          send_queue.put("tyes")
        flag = True
        break
  print("sending rainfall confirmation")

def receive_data(receive_queue,send_queue):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    if not receive_queue.empty():
      message = receive_queue.get()
      print("inside receive data")
      print(message)
      receive_queue.task_done()
      if message != "out" or message != "tri":
        if message[0] == 'r' and not rain_flag:
          rain_val = remove_character(message,'r')
          rain_flag = True
        elif message[0] == 'p'and not pool_flag:
          pool_val = remove_character(message,'p')
          pool_flag = True
  for x in range(4):
    send_queue.put("ryes")
  return (rain_val, pool_val)


def send_outfall_conf(receive_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while not receive_queue.empty():
      sleep(random.random())
      message = receive_queue.get()
      print("inside send_outfall confirmation")
      print(message)
      receive_queue.task_done()
      if message == "out":
        for x in range(4):
          send_queue.put("oyes")
        flag = True
        break
  print("sending outfall confirmation")


def detect_rain(receive_queue,send_queue):
  while True:
    print("waiting on rainfall")
    send_confirmation(receive_queue,send_queue)
    start_timeDate = datetime.datetime.now()
    print("waiting on the data")
    rain_fall, pool_level = receive_data(receive_queue,send_queue)
    end_timeDate = datetime.datetime.now() 
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    print("Rain: %s and Pool_level: %s " %(rain_fall, pool_level))
    print('start_time: %s and endtime: %s\n' %(start_time, end_time))

def detect_outfall(receive_queue,send_queue):
  while True:
    print("waiting for outfall")
    send_outfall_conf(receive_queue,send_queue)
    sleep(200)

def transmission(xbee):
  while True:
    xbee.receive_message()
    xbee.send_message()

def main():
    try:
        receive_queue = Queue.Queue()
        send_queue = Queue.Queue()
        xbee_port = xbee_usb_port()
        if xbee_port != None:
            bravo_xbee = Transceiver(9600,xbee_port,receive_queue,send_queue)
            print("starting the threads")
            t = Thread(target=detect_rain, args=(receive_queue,send_queue,))
            t.start()
            t1 = Thread(target=transmission, args =(bravo_xbee,))
            t1.setDaemon(True)
            t1.start()
            detect_outfall(receive_queue,send_queue)
        else:
            print("Check the Xbee connection")
    except KeyboardInterrupt:
            print("Ending the Program")
            t.join()
            t1.join()

if __name__ == "__main__":
  main()
