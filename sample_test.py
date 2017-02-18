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


global RESTART_HOLD 
RESTART_HOLD = 3
global COLLECT_TIME
COLLECT_TIME = 1 #minutes

level = 2.3
rain = 3.2

## gpio pins used 
buzzers = [4,17,22,5,6,13] ## wiring in beardboard
complete = 21 
mute = 20
miss = 16
restart = 12

gpio.setmode(gpio.BCM)
gpio.setup(complete,gpio.IN)
gpio.setup(mute,gpio.IN)
gpio.setup(miss,gpio.IN)
gpio.setup(restart,gpio.IN)



def check_complete():
  return not gpio.input(complete)

def check_miss():
  return not gpio.input(miss)

def check_mute():
  return not gpio.input(mute)

def check_restart():
  return not gpio.input(restart)

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
  '''
  Search in your file directory to find usb port 
  that your lcd screen is connected. 
  Supports Mac and Linux operating system 
  Returns a port
  '''
  port =  glob.glob('/dev/ttyACM*')
  return port[0]

def xbee_usb_port():
  '''
  Search in your file directory to find usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a port
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

def logger(time, amount_rain, pool_level, tag=None, outfall=None, status=None):
  directory = '~/Desktop/log_data/'
  if not os.path.exists(directory):
    os.system('mkdir ' + directory)
  date_message = '%s/%s/%s' %(time.month, time.day, time.year)
  time_message = '%s:%s:%s' %(time.hour,time.minute,time.second)
  file_name = '%s-%s-%s' %(time.month, time.day, time.year)
  if tag == 'C':
    collect_datafile = directory + file_name+'_completed.csv'
  elif tag == 'M':
    collect_datafile = directory + file_name+'_missed.csv'
  else:
    collect_datafile = directory + file_name+'.csv'

  if os.path.exists(collect_datafile):
    fopen = open(collect_datafile, 'a')
  else:
    fopen = open(collect_datafile, 'w')
  fopen.write("{},{},{},{},{},{}".format(date_message, time_message, amount_rain 
                                         ,pool_level, outfall, status))
  fopen.write("\n")
  fopen.close()

def invoke_system(led_matrix,lcd):
  count_row = 1
  invoke_color = led_matrix.ingram_colors("yellow")
  led_matrix.change_color(led_matrix.get_yellowImage())
  start_buzzer()
  row_duration  = 1.875*COLLECT_TIME
  max_time = 15*COLLECT_TIME  #change 15 to 60
  current_time = 0
  start_time = time()
  while current_time <= max_time:
    if check_complete():
      lcd.send_command("CLEAR")
      lcd.complete_message()
      complete_state(led_matrix)
      break
    if check_mute():
      stop_buzzer()
    if check_restart():
      restart_state(lcd)
    current_time = time() - start_time
    lcd.display_timer(max_time-current_time)
    if current_time >= row_duration*count_row:
          led_matrix.change_color_row(invoke_color,led_matrix.get_red(),count_row)
          count_row += 1

  if count_row >= 8: 
    lcd.send_command("CLEAR")
    lcd.missed_message()
    missed_state(led_matrix)
    lcd.send_command("CLEAR")

    
def complete_state(led_matrix):
  #grab the amount of rain 
  #grab the holding level  
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  pool_level = level # sample value
  amount_rain = rain  #sample value
  status = "completed"   #sample value
  time = datetime.datetime.now() 
  logger(time,amount_rain, pool_level, outfall, status)
  ## next_month = calculate_nextmonth()
  ## sleep(next_month)

def missed_state(led_matrix):
  #  grab the amount of rain 
  #  grab the holding level 
  #  grab the outfall  
  #  grab the time and date
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  pool_level = level # sample value
  amount_rain = rain  #sample value
  status = "missed"   #sample value #sample value
  time = datetime.datetime.now() 
  logger(time,amount_rain, pool_level, outfall, status)
  while not check_miss():
    pass
  led_matrix.change_color(led_matrix.get_greenImage())
  
def restart_state(lcd):
 state  = 0
 start_time = time()
 end_time = 0
 lcd.send_command('CLEAR')
 while end_time < RESTART_HOLD:
  end_time = time() - start_time
  lcd.holding_restart(end_time)
  state = check_restart()
  if not state:
    return
  lcd.send_command('CLEAR')
  lcd.restart_message()
  print("reset") #os.system("sudo reboot")

def checkmonth_sample():
  date_time = datetime.datetime.now()
  value  = None 
  complete_files = glob.glob('~/Desktop/log_data/' + date_time.month + '*' + date_time.year + 'C.csv')
  miss_files = glob.glob('~/Desktop/log_data/' + date_time.month + date_time.day + date_time.year + 'M.csv')

  if len(complete_files) > 0:
    value = 1
    return value
  if len(miss_files) > 0:
    value = 0
    return value

  return value

def calculate_nextday():
  time =  datetime.datetime.now()
  hour_sec = (24 - time.hour) * 60 * 60
  minute_sec = (60-time.minute) * 60
  second_sec = (60-time.second)
  total_sleep = hour_sec + minute_sec + second_sec
  return total_sleep
  
def calculate_nextmonth():
  time = datetime.datetime.now()
  hour_sec = (24-time.hour) *60 *60
  minute_sec = (60 - time.minute) * 60
  second_sec = (60-time.second)
  month_range = monthrange(time.year,time.month)
  total_days = month_range[1]
  day_sec = (total_days - time.day) *24*60*60
  total_sleep = day_sec + second_sec + minute_sec + hour_sec
  return total_sleep

def flow_sensor(status):
  ##create sender and receiver thread
  # try:
  #   message = bravo_xbee.receive_message()
  #   if message == "b":
  #     for i in range(3):
  #       bravo_xbee.send_message("a\n")
  #     invoke_system(led_matrix, lcd)
  #     bravo_xbee.clear_serial()
  # except KeyboardInterrupt:
  #   lcd.send_command("CLEAR")
  #   led_matrix.clear_matrix()
  #   stop_buzzer()
  #   gpio.cleanup()
  pass

def rain_gauge():
  ## create sender and receiver thread
  pass

def sender():
  pass

def receiver():
  pass


