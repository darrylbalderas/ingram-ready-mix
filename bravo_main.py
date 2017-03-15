import os
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from bravo_test import *
from threading import Thread
from threading import Lock

if __name__ == "__main__":
  try:
    lock = Lock()
    initialize_files()
    xbee_port = xbee_usb_port()
    lcd_port = lcd_serial_port()
    if xbee_port != None and lcd_port != None:
      bravo_xbee = Transceiver(9600,xbee_port)
      initalize_buzzers(buzzers)
      led_matrix = LedMatrix()
      lcd = LCD(lcd_port,9600)
      led_matrix.change_color(led_matrix.get_greenImage())
      lcd.welcome_message()
      thread1 = Thread(target=outfall_detection, args=(bravo_xbee,lcd,led_matrix,lock,))
      thread2 = Thread(target=rain_detection, args=(bravo_xbee,lock,))
      thread1.start()
      thread2.start()
      thread1.join()
      thread2.join()
    else:
      print("Check the Xbee and LCD connection")
  except KeyboardInterrupt:
    stop_buzzer()
    led_matrix.clear_matrix()
    bravo_xbee.clear_serial()
    lcd.send_command('CLEAR')
