import sys
import RPi.GPIO as gpio
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from buzzer import Buzzer
from ledmatrix import LedMatrix



def lcd_serial_port():
  port =  glob.glob('/dev/ttyACM*')
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


def invoke_system(buzzer1,buzzer2,buzzer3,buzzer4,led_matrix, yellow):
  buzzer1.start()
  buzzer2.start()
  buzzer3.start()
  buzzer4.start()
  led_matrix.change_color(color)

def reset_button(buzzer1,buzzer2,buzzer3,buzzer4,led_matrix, green):
  buzzer1.stop()
  buzzer2.stop()
  buzzer3.stop()
  buzzer4.stop()
  led_matrix.change_color(color)
  
  


xbee_port = xbee_usb_port()
lcd_port = lcd_serial_port()
lcd = LCD(lcd_port,9600)
bravo_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
buzzer1 = Buzzer(12, "BCM")
buzzer2 = Buzzer(16,"BCM")
buzzer3 = Buzzer(20, "BCM")
buzzer4 = Buzzer(21,"BCM")
led_matrix = LedMatrix()

color_images = led_matrix.get_color_images()
yellow = color_images['yellow']
green = color_images['green']
red = color_images['red']
led_matrix.clear_matrix()

flag = False
message = ""
while not flag:
  bravo_xbee.receive_message()

  if message == "rain\n":
    print("yes")

  





gpio.cleanup()
