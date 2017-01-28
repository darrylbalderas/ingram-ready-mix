import os 
import time 
import sys 
from transmitter import Transmitter
from lcd import LCD
import glob
import serial
from time import sleep

def xbee_Usb_Port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
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

def lcd_serial_port():
	port =  glob.glob('/dev/tty.usbmodem*')
	return port[0]

def main():
  xbee_port = xbee_Usb_Port()
  lcd_port = lcd_serial_port()
  lcd = LCD(lcd_port,9600)
  xbee = Transmitter(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x03\xF0\xFF")
  messgae = " "
  flag = False
  print("Start process")
  while not flag:
    message = xbee.receive_message()
    print("1 :  " + message)
    if message != "": 
      lcd.send_message(message)
      xbee.send_message("got it")


if __name__ == "__main__":
	main()


