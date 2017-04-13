'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This program was written to implement a alarm system in 
conjunction with the outfall detection system for the ingram 
ready mix plant
'''

# transceiver is a module that contains all of the functions
# and initialization of the Xbee module. 
from transceiver import Transceiver

#lcd is a module that contains all of the functions and 
# variables corresponding to the LCD screed 
from lcd import LCD

# led matrix is a module that contains all of the function 
# and variables corresponding to the Sense hat hardware
from ledmatrix import LedMatrix

from threading import Thread
from threading import Event
from threading import Lock 

# bravo test is a module that contains all of the function 
# for alarm system 
import bravo_test as bt
import RPi.GPIO as gpio

def main():
  event = Event() # use as a flag for ending all of the threads at once
  lock = Lock()
  send_queue= [ ]
  out_queue = [ ]
  trigger_queue = [ ]
  data_queue = [ ]
  voltage_queue = [ ]
  bt.initialize_files()
  xbee_port = bt.xbee_usb_port()
  lcd_port = bt.lcd_serial_port()
  if xbee_port != None and lcd_port != None:
    bravo_xbee = Transceiver(9600,xbee_port,out_queue,trigger_queue,data_queue,voltage_queue,send_queue)
    bt.initalize_buzzers()
    led_matrix = LedMatrix()
    lcd = LCD(lcd_port,9600)
    led_matrix.change_color(led_matrix.get_greenImage())
    lcd.welcome_message()
    thread1 = Thread(target=bt.outfall_detection, args=(lcd,led_matrix,out_queue,send_queue,event,lock,))
    thread1.start()
    thread2 = Thread(target=bt.rain_detection, args=(trigger_queue,data_queue,voltage_queue,send_queue,event,lock,))
    thread2.start()
    bt.transmission(bravo_xbee,event)
    # thread3 = Thread(target=bt.transmission, args = (bravo_xbee,event,))
    # thread3.start()
##    while not event.is_set():
##      user_input = raw_input("Enter (Y) or (N) to stop program: ")
##
##      if user_input.lower() == 'y':
##            print("Ending the Program")
##            event.set()
##            thread1.join()
##            thread2.join()
##            thread3.join()
##            gpio.cleanup()
##            bt.stop_buzzer()
##            led_matrix.clear_matrix()
##            bravo_xbee.clear_serial()
##            lcd.send_command('CLEAR')
  else:
      print("Check the Xbee and LCD connection")
if __name__ == "__main__":
  main()
