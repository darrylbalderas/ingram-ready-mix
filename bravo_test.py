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
import math


global RESTART_HOLD 
RESTART_HOLD = 3
global COLLECT_TIME
COLLECT_TIME = 15 #minutes

os.eviron['pool_level'] = 0
os.environ['rain'] = 0

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

def logger(start_time, end_time, amount_rain, pool_level, tag=None, outfall=None, status=None):
  directory = '~/Desktop/log_data/'
  time_date = datetime.datetime.now()
  if not os.path.exists(directory):
    os.system('mkdir ' + directory)
  # date_message = '%s/%s/%s' %(time_date.month, time_date.day, time_date.year)
  file_name = '%s-%s-%s' %(time_date.month, time_date.day, time_date.year)
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
    fopen.write('StartTime, EndTime, AmountRain, PoolLevel, Outfall, Status')
  fopen.write("{},{},{},{},{},{}".format(start_time, end_time, amount_rain 
                                         ,pool_level, outfall, status))
  fopen.write("\n")
  fopen.close()

def invoke_system(led_matrix,lcd):
  #create an enviroment variable for invoke system
  os.environ['invoke'] = 1
  os.environ['restart'] = 0
  start_buzzer()
  count_row = 1
  invoke_color = led_matrix.ingram_colors("yellow")
  led_matrix.change_color(led_matrix.get_yellowImage())
  row_duration  = 1.875*COLLECT_TIME
  max_time = 15*COLLECT_TIME  #change 15 to 60
  current_time = 0
  timer = time()
  time_date = datetime.datetime.now()
  start_time = time_date.month() + ':' + time_date.day() + ':' + time_date.year()
  while current_time <= max_time:
    if check_complete():
      lcd.complete_message()
      if os.environ['restart'] != 0:
        complete_state(led_matrix,start_time)
        os.environ['invoke'] = 0
        return 
      break
    if check_mute():
      stop_buzzer()
    if check_restart():
      restart_state(lcd)
    current_time = time() - timer
    lcd.display_timer(max_time-current_time)
    if current_time >= row_duration*count_row:
          led_matrix.change_color_row(invoke_color,led_matrix.get_red(),count_row)
          count_row += 1
  if count_row >= 8: 
    lcd.missed_message()
    missed_state(led_matrix,start_time)
  else:
    led_matrix.change_color(led_matrix.get_greenImage())

 
def complete_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  pool_level = os.environ['pool_level'] # sample value
  amount_rain = os.environ['rain']  #sample value
  status = "completed"   #sample value 
  time_date = datetime.datetime.now()
  end_time =  time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  logger(start_time, end_time, amount_rain, pool_level, outfall, status)

def missed_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  pool_level = os.environ['pool_level'] 
  amount_rain = os.environ['rain']
  status = "missed"   #sample value #sample value
  time_date = datetime.datetime.now() 
  end_time =  time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  logger(start_time, end_time ,amount_rain, pool_level, outfall, status)
  while not check_miss():
    pass
  led_matrix.change_color(led_matrix.get_greenImage())
  
def restart_state(lcd):
  lcd.send_command('CLEAR')
  state  = 0
  end_time = 0
  start_time = time()
  while end_time < RESTART_HOLD:
    end_time = time() - start_time
    lcd.holding_restart(end_time)
    state = check_restart()
    if not state:
      return
  lcd.restart_message()
  os.environ['restart'] = 1
  print("reset")  # for testing purposes
  # os.system("sudo reboot")

def checkmonth_sample():
  time_date = datetime.datetime.now()
  complete_files = glob.glob('~/Desktop/log_data/' + time_date.month + '*' + time_date.year + 'C.csv')
  miss_files = glob.glob('~/Desktop/log_data/%s-%s-%sM.csv'%(time_date.month,
                                                              time_date.day, time_date.year))
  if len(complete_files) > 0:
    return 1
  elif len(miss_files) > 0:
    return 0
  else:
    return None

def calculate_sleep(state):
  flag = False
  time_date = datetime.datetime.now()
  if state == False:
    interval =  24 - time_date.hour
    if interval > 0:
      flag = True
  elif state == True:
    days_left = monthrange(time_date.year,time_date.month)
    interval = days_left[1] - time_date.day
    if interval > 0:
      flag = True
  return flag
  
def detect_rain(xbee,lcd):
  pool_level = ""
  activation = ""
  rain_fall = ""
  while activation != "":
    ## include waiting message 
    ## include mutex lock to ensure full usage of lcd
    activation = xbee.receive_message()

  xbee.clear_serial()
  time_date = datetime.datetime.now()
  start_time = time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  while pool_level !=  "":
    ## include waiting message 
    ## include mutex lock to ensure full usage of lcd
    pool_level = xbee.receive_message()
    xbee.send_message('stop\n')

  xbee.clear_serial()
  os.environ['pool_level'] = float(pool_level)
  while rain_fall != "":
    ## include waiting message 
    ## include mutex lock to ensure full usage of lcd
    rain_fall = xbee.receive_message()
    xbee.send_message('stop\n')

  xbee.clear_serial()
  os.environ['environ'] = float(rain_fall)
  end_time = time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  logger(start_time,end_time,rain_fall,pool_level,None,"-","-")
