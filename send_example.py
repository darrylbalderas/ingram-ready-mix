import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep
import os

STATUS = './status_val.txt'
INVOKE = './invoke_val.txt'
INVOKE_DATE = './invoke_date_val.txt'
RAIN = './rain_val.txt'
POOL_LEVEL = './pool_level_val.txt'
RESTART = './restart_val.txt'

arrays = [STATUS,INVOKE, INVOKE_DATE, RAIN, POOL_LEVEL, RESTART]

def initialize_files(arrays):
  for array in arrays:
    fopen = open(array, 'w')
    fopen.write('0')
    fopen.close()

def xbee_usb_port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
    
  for port in ports:
      try:
          ser = serial.Serial(port)
          ser.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass
  return result[0]

def outfall_detection(xbee):
    outfall_confirmation = ""
    while outfall_confirmation != 'stop':
      outfall_confirmation = xbee.receive_message()
      print(outfall_confirmation + 'nope')
      xbee.send_message('out\n')


# port = xbee_usb_port()
# charlie_xbee = Transceiver(9600,port)
# outfall_detection(charlie_xbee)
initialize_files(arrays)
