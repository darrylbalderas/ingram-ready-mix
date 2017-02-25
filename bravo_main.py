import os
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from bravo_test import *


if __name__ == "__main__":
  try:
    initialize_files()
    initalize_buzzers(buzzers)
    led_matrix = LedMatrix()
    led_matrix.change_color(led_matrix.get_greenImage())
    xbee_port = xbee_usb_port()
    lcd_port = lcd_serial_port()
    lcd = LCD(lcd_port,9600)
    #lcd.welcome_message()
    bravo_xbee = Transceiver(9600,xbee_port)#,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
    detect_rain(bravo_xbee)
  except KeyboardInterrupt:
    stop_buzzer()
    led_matrix.clear_matrix()
    bravo_xbee.clear_serial()
    lcd.send_command('CLEAR')
  ##create rainfall_detection thread
  ## pass the rainfall detection function 
  ##create outfall detection thread
  ## pass the outfall detection thread 
  pass
