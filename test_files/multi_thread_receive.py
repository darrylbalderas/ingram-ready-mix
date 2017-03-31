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

def send_confirmation(tri_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while len(tri_queue) != 0:
      message = tri_queue.pop(0)
      if message == "tri":
        send_queue.append("tyes")
        flag = True
        break

def receive_data(data_queue,send_queue):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    if len(data_queue) != 0:
      message = data_queue.pop(0)
      if message != "out" or message != "tri":
        if message[0] == 'r' and not rain_flag:
          rain_val = remove_character(message,'r')
          rain_flag = True
        elif message[0] == 'p'and not pool_flag:
          pool_val = remove_character(message,'p')
          pool_flag = True
  send_queue.append("ryes")
  return (rain_val, pool_val)


def send_outfall_conf(out_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        send_queue.append("oyes")
        flag = True
        break


def detect_rain(tri_queue,data_queue,send_queue):
  while True:
    send_confirmation(tri_queue,send_queue)
    # start timer
    rain_fall, pool_level = receive_data(data_queue,send_queue)
    # end timer

def detect_outfall(out_queue,send_queue):
  while True:
    send_outfall_conf(out_queue,send_queue)

def transmission(xbee):
  while True:
      xbee.receive_message()
      xbee.send_message()

def main():
    try:
        send_queue= []
        out_queue = []
        tri_queue = []
        data_queue = []
        xbee_port = xbee_usb_port()
        if xbee_port != None:
            bravo_xbee = Transceiver(9600,xbee_port,out_queue,tri_queue,data_queue, send_queue)
            t = Thread(target=detect_rain, args=(tri_queue,data_queue,send_queue,))
            t.start()
            t1 = Thread(target=transmission, args =(bravo_xbee,))
            t1.start()
            detect_outfall(out_queue,send_queue)
        else:
            print("Check the Xbee connection")
    except KeyboardInterrupt:
            t.join()
            t1.join()

if __name__ == "__main__":
  main()
