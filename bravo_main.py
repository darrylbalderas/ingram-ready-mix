# import os
# from time import sleep
# import glob
# import serial
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
    lcd.welcome_message()
    bravo_xbee = Transceiver(9600,xbee_port)
    #create two threads
    # rain_detection(bravo_xbee) # thread 1
    # outfall_detection(bravo_xbee,lcd,led_matrix) # thread 2
  except KeyboardInterrupt:
    stop_buzzer()
    led_matrix.clear_matrix()
    bravo_xbee.clear_serial()
    lcd.send_command('CLEAR')
  pass
