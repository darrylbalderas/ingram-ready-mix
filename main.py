import sys
import os
from time import sleep
import glob
import serial
# from transceiver import Transceiver
# from lcd import LCD
# from ledmatrix import LedMatrix
from time import time
import datetime
from calendar import monthrange
from bravo_test import *

def outfall_detection():
  os.environ['status'] = None
  os.environ['restart'] = 0
  initalize_buzzers(buzzers)
  xbee_port = xbee_usb_port()
  lcd_port = lcd_serial_port()
  lcd = LCD(lcd_port,9600)
  lcd.welcome_message()
  bravo_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
  led_matrix = LedMatrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  while True:
    outfall = ""
    os.environ['status'] = str(checkmonth_sample())
    if os.environ['status'] == '1':
      while calculate_sleep(True):
        if check_restart():
          restart_state()
        pass
    elif os.environ['status'] == '0':
      while calculate_sleep(False):
        if check_restart():
          restart_state()
        pass
    elif os.environ['status'] == None:
      outfall = bravo_xbee.receive_message()
      if outfall == 'out':
        time_date = datetime.datetime.now()
        restart_date = time_date.month+'/'+time_date.year
        if os.environ['restart'] == '1' and restart_date == os.environ[invoke_date]:
          invoke_system(led_matrix, lcd)
        elif os.environ['invoke'] == '0' and os.environ['restart'] == '0':
          invoke_system(led_matrix, lcd)

      

if __name__ == "__main__":
  ##create rainfall_detection thread
  ## pass the rainfall detection function 
  ##create outfall detection thread
  ## pass the outfall detection thread 
  pass