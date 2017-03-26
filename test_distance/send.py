import sys
import os
from transceiver import Transceiver
import serial 
import glob 
from time import sleep 

def xbee_usb_port():
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyUSB0*')
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

def detect_outfall(xbee):
  count = 0
  message = ""
  while True:
    xbee.send_message('out\n')
    sleep(0.5)
    count += 1
    message = xbee.receive_message()
    print(message)
    if message == 'oyes':
      print(count)
      break

port = xbee_usb_port()
xbee = Transceiver(9600,port)
while True:
  message = raw_input('Enter the trigger:')
  if message == 'y':
    print("sending the message")
    detect_outfall(xbee)
