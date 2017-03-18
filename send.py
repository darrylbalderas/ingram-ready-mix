import sys
import os
from transceiver import Transceiver

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
  while True:
    xbee.send_message('out\n')
    sleep(0.5)
    if xbee.receive_message() == 'oyes':
      break



port = xbee_usb_port()
xbee = Transceiver(9600,port)
while True:
  message = raw_input('Enter the trigger:')
  if message == 'y':
    detect_outfall(xbee)