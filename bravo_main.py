import os
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from bravo_test import *
from threading import Thread

if __name__ == "__main__":
  try:
    send_queue= []
    out_queue = []
    tri_queue = []
    data_queue = []
    voltage_queue = []
    initialize_files()
    xbee_port = xbee_usb_port()
    lcd_port = lcd_serial_port()
    if xbee_port != None and lcd_port != None:
      bravo_xbee = Transceiver(9600,xbee_port,out_queue,trigger_queue, data_queue, send_queue)
      initalize_buzzers(buzzers)
      led_matrix = LedMatrix()
      lcd = LCD(lcd_port,9600)
      led_matrix.change_color(led_matrix.get_greenImage())
      lcd.welcome_message()
      thread1 = Thread(target=outfall_detection, args=(lcd,led_matrix,out_queue,send_queue))
      thread2 = Thread(target=rain_detection, args=(tri_queue,data_queue,send_queue))
      thread3 = Thread(target=transmission, args = (bravo_xbee))
      thread1.start()
      thread2.start()
      thread3.start()
    else:
      print("Check the Xbee and LCD connection")
  except KeyboardInterrupt:
    print("Ending the Program")
    thread1.join()
    thread2.join()
    thread3.join()
    stop_buzzer()
    led_matrix.clear_matrix()
    bravo_xbee.clear_serial()
    lcd.send_command('CLEAR')
