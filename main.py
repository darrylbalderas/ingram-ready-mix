import sys
import os
import RPi.GPIO as gpio
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from time import time
import datetime
from calendar import monthrange
from sample_test import *
import numpy 

def main():
  ## incorporate sleep month or day functionality  
  initalize_buzzers(buzzers)
  xbee_port = xbee_usb_port()
  lcd_port = lcd_serial_port()
  lcd = LCD(lcd_port,9600)
  lcd.welcome_message()
  bravo_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
  led_matrix = LedMatrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  while True:
    status = checkmonth_sample()
    if status == 1:
      ## check the remainder of days for the next month 
      ## create a while loop that will iterate over this days 
      ## inside the while loop record time, rainfall, pool level
      pass
    elif status == 0:
      ## check the remainder of hours for the next day
      ## create a while loop that will iterate over this days 
      ## inside the while loop record time, rainfall, pool level
      pass
    else:
      ## full system check
      pass