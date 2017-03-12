
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

def remove_character(message,character):
    return message.strip(character)

def receive_data(xbee):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not rain_flag and not pool_flag:
    message = xbee.receive_message()
    if len(message) != 0:
      if message[0] == 'r' and not rain_flag:
        rain_val = float(remove_character(message))
        rain_flag = True
      elif message[0] == 'p' and not pool_flag:
        pool_val = float(remove_character(message))
        pool_flag = True
    xbee.send_message("no\n")

  xbee.send_message("yes\n")


def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  message = ""
  try:
    while not message == 'tri':
      message = xbee.receive_message()
      print(message)

    xbee.send_message("yes\n")
    sleep(0.5)
  except KeyboardInterrupt:
    print("\nexit")

if __name__ == "__main__":
  main()
