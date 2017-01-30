import sys
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

buzzers = [4,17,22,5,6,13] ## wiring in beardboard
complete = 21 
mute = 20
miss = 16
yellow = [255,135,0]
green = [0,255,0]
red = [255,0,0]

gpio.setmode(gpio.BCM)
gpio.setup(complete,gpio.IN)
gpio.setup(mute,gpio.IN)
gpio.setup(miss,gpio.IN)

miss_message="missed sample   "
complete_message = "complete sample "
restart_message = "Restart system  "

comm_message = "Comm establish  "
nocomm_message = "NoComm establish"


def check_complete():
  return not gpio.input(complete)

def check_miss():
  return not gpio.input(miss)

def check_mute():
  return not gpio.input(mute)

def initalize_buzzers(buzzers):
  for buzzer in buzzers:
    gpio.setup(buzzer,gpio.OUT)

def start_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,True)

def stop_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,False)

  
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

def make_newcolor(color):
  image = []
  for i in range(64):
    if color.lower() == "yellow":
      image.append(yellow)
    elif color.lower() == "red":
      image.append(red)
    elif color.lower() == "green":
      image.append(green)
  return image

def fappend_blanks(message):
  '''
  appends blank spaces in the beginning of the message
  '''
  if len(message) != 16:
    blanks = 16 - len(message)
    return (blanks*" " + message)

def bappend_blanks(message):
  '''
  appends blanks spaces at the end of the message
  '''
  if len(message) != 16:
    blanks = 16 - len(message)
    return (blanks*" " + message)

def print_message(num_time,voltage,lcd):
  time_m = "{0:.3f}\r".format(num_time)
  lcd.send_message(time_m)
  message = fappend_blanks(str(voltage)+'V')
  lcd.send_message(message)
  lcd.send_command("HOME")

def invoke_system(led_matrix,color_array, colors,lcd):
  voltage = 5
  minutes = 2
  invoke_color = make_newcolor("yellow")
  led_matrix.change_color(invoke_color)
  start_buzzer()
  row_duration  = 1.875*minutes
  count_row = 1
  max_time = 15*minutes
  previous_time = time()
  current_time = 0
  while current_time <= max_time:
    if check_complete():
      count_row = 1
      lcd.send_command("CLEAR")
      lcd.send_message(complete_message)
      complete_state(led_matrix,color_array)
      break

    if check_mute():
      stop_buzzer()
    
    current_time = time() - previous_time
    print_message(current_time,voltage,lcd)
    if current_time >= row_duration*count_row:
          led_matrix.change_color_row(invoke_color,colors[1], count_row)
          count_row += 1

  if count_row >= 8:  ## change to a wait statement
    lcd.send_command("CLEAR")
    lcd.send_message(miss_message)
    missed_state(led_matrix,color_array)
    lcd.send_command("CLEAR")
    #change ledmatrix to green 


  

def complete_state(led_matrix,color_array):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(color_array[0])
  ## create a log 
  ## open logger
  ##record data and put complete to the log 
  ##calculate the time need for the rest of the month and sleep for that 
  ## amount of time

def missed_state(led_matrix, color_array):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(color_array[1])
  ## create a logger
  ## open logger
  ## recorde data and put missed to the log
  ## close logger
  ## calculate the time need for the rest of the day and sleep for that
  #amount of time
  while not check_miss():
    pass


def restart_state():
  ## do a system command to restart system
  pass


  


def main():
   initalize_buzzers(buzzers)
   xbee_port = xbee_usb_port()
   lcd_port = lcd_serial_port()
   lcd = LCD(lcd_port,9600)
   bravo_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
   led_matrix = LedMatrix()
    
   color_images = led_matrix.get_color_images()
   color_info = led_matrix.get_colors()
   color_array = [color_images['green'], color_images['red'], color_images['yellow']]
   colors = [color_info['g'], color_info['r'], color_info['y']]
   led_matrix.change_color(color_array[0])
   while True:
     try:      
       message = bravo_xbee.receive_message()
       if message == "b":
         for i in range(3):
           bravo_xbee.send_message("a\n")
         invoke_system(led_matrix,color_array,colors,lcd)
      
     except KeyboardInterrupt:
       lcd.send_command("CLEAR")
       led_matrix.clear_matrix()
       stop_buzzer()
       gpio.cleanup()
       break
   gpio.cleanup()

def calculate_nextday():
  time =  datetime.datetime.now()
  hour_sec = (24 - time.hour) * 60 * 60
  minute_sec = (60-time.minute) * 60
  second_sec = (60-time.second)
  total_sleep = hour_sec + minute_sec + second_sec
  
  return total_sleep
   
def calculate_nextmonth():
  #time object
  time = datetime.datetime.now()
  
  #the values for the time object
  hour_sec = (24-time.hour) *60 *60
  minute_sec = (60 - time.minute) * 60
  second_sec = (60-time.second)

  #calculates the number
  month_range = monthrange(time.year,time.month)
  total_days = month_range[1]
  
  day_sec = (total_days - time.day) *24*60*60

  total_sleep = day_sec + second_sec + minute_sec + hour_sec
  
  return total_sleep


if __name__ == '__main__':
