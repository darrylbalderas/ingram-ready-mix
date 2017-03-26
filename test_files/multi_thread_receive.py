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

##complete = 12 
##mute = 20
##miss = 16
##restart = 21
##gpio.setmode(gpio.BCM)
##gpio.setup(complete,gpio.IN)
##gpio.setup(mute,gpio.IN)
##gpio.setup(miss,gpio.IN)
##gpio.setup(restart,gpio.IN)
##
##def check_complete():
##    return gpio.input(complete)
##
##def check_miss():
##    return gpio.input(miss)
##
##def check_mute():
##    return gpio.input(mute)
##
##def check_restart():
##    return gpio.input(restart)
##
##def check_buttons():
##    print("This is the value for complete button: %d" %(check_complete()))
##    print("This is the value for missed button: %d" %(check_miss()))
##    print("This is the value for mute button: %d" %(check_mute()))
##    print("This is the value for restart button: %d" %(check_restart()))
##    print('\n\n')

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

def send_confirmation(xbee,lock):
  message = ""
  while not message == 'tri':
    lock.acquire()
    message = xbee.receive_message()
    lock.release()
    sleep(0.25)
  lock.acquire()
  xbee.send_message("tyes\n")
  sleep(0.25)
  lock.release()
  sleep(0.25)

def receive_data(bravo_xbee,lock):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    message = bravo_xbee.receive_message()
    print(message)
    if len(message) > 1:
      if message[0] == 'r' and not rain_flag:
        rain_val = bravo_xbee.remove_character(message,'r')
        rain_flag = True
      elif message[0] == 'p'and not pool_flag:
        pool_val = bravo_xbee.remove_character(message,'p')
        pool_flag = True
    bravo_xbee.send_message("rno\n")
    sleep(0.25)
  bravo_xbee.send_message("ryes\n")
  sleep(0.25)
  return (rain_val, pool_val)

def detect_rain(bravo_xbee,lock):
  while True:
    send_confirmation(bravo_xbee,lock)
    print("got first rain confirmation")
    start_timeDate = datetime.datetime.now()
    send_confirmation(bravo_xbee,lock)
    print("got second rain confirmation")
    lock.acquire()
    rain_fall, pool_level = receive_data(bravo_xbee)
    lock.release()
    print("got pool and rain data")
    end_timeDate = datetime.datetime.now() 
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    print("Rain: %s and Pool_level: %s " %(rain_fall, pool_level))
    print('start_time: %s and endtime: %s\n' %(start_time, end_time))

def send_outfall_conf(xbee,lock):
  message = ""
  while not message == 'out':
    lock.acquire()
    message = xbee.receive_message()
    lock.release()
    sleep(0.25)
  print("got the outfall trigger")
  lock.acquire()
  xbee.send_message("oyes\n")
  sleep(0.25)
  lock.release()
  sleep(0.25)
  print("sending outfall confirmation")

def detect_outfall(bravo_xbee,lock):
  while True:
    send_outfall_conf(bravo_xbee,lock)

def main():
    try:
        lock = Lock()
        xbee_port = xbee_usb_port()
        if xbee_port != None:
            bravo_xbee = Transceiver(9600,xbee_port)
            print("starting the threads")
            p2 = Process(target=detect_rain, args=(bravo_xbee,lock,))
            p2.start()
            detect_outfall(bravo_xbee,lock)
        else:
            print("Check the Xbee connection")
    except KeyboardInterrupt:
            print("Ending the Program")
            # thread1.join()
            p2.join()

if __name__ == "__main__":
  main()
