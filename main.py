import os 
from time import time
import sys 
from transceiver import Transceiver
from lcd import LCD
import glob
import serial
from time import sleep

def find_ports():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usb*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/tty[A-Za-z]*')

  for port in ports:
      try:
          ser = serial.Serial(port)
          ser.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass
  return result[0]


def fappend_blanks(message):
  '''
  appends blank spaces in the beginning of the message
  '''
  if len(message) != 16:
    blanks = 16 - len(message)
    return (blanks*" " + message)

def bappend_blanks(message):
  '''
  appends blanks spaces at the end of the message
  '''
  if len(message) != 16:
    blanks = 16 - len(message)
    return (blanks*" " + message)

def move_cursor(lcd,spaces):
  for num in range(spaces):
    lcd.send_command("MOVE_CURSOR")

def print_message(num_time,voltage,lcd):
  time_m = "{0:.3f}\r".format(num_time)
  lcd.send_message(time_m)
  message = fappend_blanks(str(voltage)+'V')
  lcd.send_message(message)
  lcd.send_command("HOME")

def main():
  port = find_ports()
  lcd = LCD(port,9600)


if __name__ == "__main__":
	main()


