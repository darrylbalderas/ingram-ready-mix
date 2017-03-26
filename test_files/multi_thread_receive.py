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

class Job(object):
    def __init__(self, priority, message):
        self.priority = priority
        self.description = message
    def __cmp__(self, other):
        return cmp(self.priority,other.priority)

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
      job = receive_queue.get()
      message = job.description
      if message == "tri":
        print("received trigger")
        for x in range(4):
          send_queue.put(Job(2,"tyes"))
        flag = True
        break
      elif message == "out":
        sleep(1)
  print("sending rainfall confirmation")

def receive_data(receive_queue,send_queue):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    if not receive_queue.empty():
      job = receive_queue.get()
      message = job.description
      if message != "out" or message != "tri":
        if message[0] == 'r' and not rain_flag:
          rain_val = remove_character(message,'r')
          rain_flag = True
        elif message[0] == 'p'and not pool_flag:
          pool_val = remove_character(message,'p')
          pool_flag = True
      else:
        sleep(1)
  for x in range(6):
    send_queue.put(Job(2,"ryes"))
  return (rain_val, pool_val)


def send_outfall_conf(receive_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while not receive_queue.empty():
      job = receive_queue.get()
      message = job.description
      if message == "out":
        for x in range(6):
          send_queue.put(Job(1, "oyes"))
        flag = True
        break
      elif message == "tri":
        sleep(1) 
  print("sending outfall confirmation")


def detect_rain(receive_queue,send_queue):
  while True:
    print("waiting on rainfall")
    send_confirmation(receive_queue,send_queue)
    start_timeDate = datetime.datetime.now()
    rain_fall, pool_level = receive_data(receive_queue,send_queue)
    end_timeDate = datetime.datetime.now() 
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    print("Rain: %s and Pool_level: %s " %(rain_fall, pool_level))
    print('start_time: %s and endtime: %s\n' %(start_time, end_time))

def detect_outfall(receive_queue,send_queue):
  while True:
    print('waiting for outfall')
    send_outfall_conf(receive_queue,send_queue)

def transmission(xbee):
  while True:
    xbee.receive_message()
    xbee.send_message()

def main():
    try:
        receive_queue = Queue.PriorityQueue()
        send_queue = Queue.PriorityQueue()
        xbee_port = xbee_usb_port()
        if xbee_port != None:
            bravo_xbee = Transceiver(9600,xbee_port,receive_queue,send_queue)
            print("starting the threads")
            t = Thread(target=detect_rain, args=(receive_queue,send_queue,))
            t1 = Thread(target=transmission, args =(bravo_xbee,))
            t1.start()
            t.start()
            detect_outfall(receive_queue,send_queue)
        else:
            print("Check the Xbee connection")
    except KeyboardInterrupt:
            print("Ending the Program")
            t.join()
            t1.join()

if __name__ == "__main__":
  main()
