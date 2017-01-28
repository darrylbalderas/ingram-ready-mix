import sys
import RPi.GPIO as gpio
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD


rain_sensor = 23
rain_guage = 18
gpio.setmode(gpio.BCM)
gpio.setup(rain_sensor,gpio.OUT)
gpio.setup(rain_guage,gpio.IN)

def lcd_serial_port():
  port =  glob.glob('/dev/tty.usbmodem*')
  return port[0]

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


xbee_port = xbee_usb_port()
lcd_port = lcd_serial_port()
lcd = LCD(lcd_port,9600)
charlie_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
while True:
    rg_state = not gpio.input(rain_guage)
    if rg_state:
        rs_state = 1
        gpio.output(rain_sensor,rs_state)
        charlie_xbee.send_message("hi")
        print("yup")
    else:
        rs_state = 0
        gpio.output(rain_sensor,rs_state)        

gpio.cleanup()
