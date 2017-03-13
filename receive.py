
import serial
from transceiver import Transceiver
import glob
import sys
from time import time
from time import sleep

def xbee_usb_port():
  '''
  Search in your file directory to find Usb port 
  that your xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial-DN01IV*')
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


def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  try:
    pass
  except KeyboardInterrupt:
    print("\nexit")

if __name__ == "__main__":
  main()
