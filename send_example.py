import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep
from test import print_hello
import os

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