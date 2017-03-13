import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep
from time import time

def xbee_usb_port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial-DN01IU*')
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

def check_status():
  char_input = ""
  while char_input != 'y':
    char_input = raw_input("Trigger the rain guage: ")

def create_trigger(xbee):
  status = False
  while not status:
    xbee.send_message('tri\n')
    message = xbee.receive_message()
    print(message)
    if message == "yes":
      status = True

def send_data(xbee):
  rain_val = 'r2.1\n' 
  #wait 7 minutes and grab the total number of rain
  pool_val = 'p1.0\n'
  message = ""
  while not message == "yes":
    xbee.send_message(rain_val)
    sleep(0.5)
    xbee.send_message(pool_val)
    sleep(0.5)
    message  = xbee.receive_message()
    print(message)

def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  try:
    check_status()
    create_trigger(xbee)
    send_data(xbee)
  except KeyboardInterrupt:
    print("\nexit")

if __name__ == "__main__":
  main()

