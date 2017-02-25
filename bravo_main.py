import os
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from bravo_test import *

if __name__ == "__main__":
  initialize_files()
  initalize_buzzers(buzzers)
  xbee_port = xbee_usb_port()
  lcd_port = lcd_serial_port()
  lcd = LCD(lcd_port,9600)
  lcd.welcome_message()
  bravo_xbee = Transceiver(9600,xbee_port)#,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
  led_matrix = LedMatrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  #outfall_detection(bravo_xbee,lcd,led_matrix)
  ##create rainfall_detection thread
  ## pass the rainfall detection function 
  ##create outfall detection thread
  ## pass the outfall detection thread 
  pass
