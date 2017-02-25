import sys
import os
import RPi.GPIO as gpio
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from time import time
import datetime
from calendar import monthrange


global RESTART_HOLD 
RESTART_HOLD = 3 #seconds 

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
  time_date = datetime.datetime.now()
  directory = '~/Desktop/log_data/'
  if not os.path.exists(directory):
    os.system('mkdir ' + directory)
  directory = directory + time_date.year + '/'
  if not os.path.exists(directory):
    os.system('mkdir ' + directory)
  directory = directory + time_date.month + '/'
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

def invoke_system(led_matrix,lcd,bravo_xbee):
  os.environ['invoke'] = '1'
  start_buzzer()
  count_row = 1
  invoke_color = led_matrix.ingram_colors("yellow")
  led_matrix.change_color(led_matrix.get_yellowImage())
  current_time = 0
  timer = time()
  time_date = datetime.datetime.now()
  start_time = time_date.month() + ':' + time_date.day() + ':' + time_date.year()
  os.environ['invoke_date'] = time.month+'/'+time.year
  while current_time <= led_matrix.get_max_time():
    bravo_xbee.send_message('stop\n')
    if check_complete():
      lcd.complete_message()
      complete_state(led_matrix,start_time)
      return 
    if check_mute():
      stop_buzzer()
    if check_restart():
      restart_state(lcd)
    current_time = time() - timer
    lcd.display_timer(led_matrix.get_max_time()-current_time)
    if current_time >= led_matrix.get_row_duration()*count_row:
          led_matrix.change_color_row(invoke_color,led_matrix.get_red(),count_row)
          count_row += 1

  if count_row >= 8: 
    lcd.missed_message()
    missed_state(led_matrix,start_time)
  else:
    stop_buzzer()
    led_matrix.change_color(led_matrix.get_greenImage())

 
def complete_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  pool_level = os.environ['pool_level'] 
  amount_rain = os.environ['rain']  
  status = "completed"  
  time_date = datetime.datetime.now()
  end_time =  time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  logger(start_time, end_time, amount_rain, pool_level, 'C', outfall, status)
  os.environ['invoke'] = '0'
  os.environ['restart'] = '0'

def missed_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  pool_level = os.environ['pool_level'] 
  amount_rain = os.environ['rain']
  status = "missed"  
  time_date = datetime.datetime.now() 
  end_time =  time_date.hour + ':' + time_date.minute + ':' + time_date.second 
  logger(start_time, end_time ,amount_rain, pool_level, 'M', outfall, status)
  os.environ['invoke'] = '0'
  os.environ['restart'] = '0'
  while not check_miss():
    pass
  led_matrix.change_color(led_matrix.get_greenImage())
  
def restart_state(lcd,led_matrix):
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
  stop_buzzer()
  lcd.restart_message()
  led_matrix.clear_matrix()
  os.environ['restart'] = '1'
  print("reset")  # for testing purposes
  # os.system("sudo reboot")

def checkmonth_sample():
  time_date = datetime.datetime.now()
  complete_dir = '~/Desktop/log_data/'+ time_date.year +'/' + time_date.month + '/*_completed.csv'
  missed_dir = '~/Desktop/log_data/'+ time_date.year +'/' + time_date.month + '/*_missed.csv'
  complete_files = glob.glob(complete_dir)
  miss_files = glob.glob(missed_dir)
  if len(complete_files) > 0:
    return 1
  elif len(miss_files) > 0:
    return 0
  else:
    return None

def calculate_sleep(status):
  sleep_flag = False
  time_date = datetime.datetime.now()
  if status == 'missed':
    time_left =  24 - int(time_date.hour)
    if time_left > 0:
      sleep_flag = True
  elif status == 'complete':
    days_left = monthrange(time_date.year,time_date.month)
    time_left = days_left[1] - int(time_date.day)
    if time_left > 0:
      sleep_flag = True
  return sleep_flag
  
def detect_rain(bravo_xbee):
  while True:
    pool_level = ""
    rain_fall = ""
    while pool_level !=  "":
      pool_level = bravo_xbee.receive_message()
      bravo_xbee.send_message('stop\n')

    bravo_xbee.clear_serial()
    time_date = datetime.datetime.now()
    start_time = time_date.hour + ':' + time_date.minute + ':' + time_date.second 
    os.environ['pool_level'] = float(pool_level)
    while rain_fall != "":
      rain_fall = bravo_xbee.receive_message()
      bravo_xbee.send_message('stop\n')

    bravo_xbee.clear_serial()
    os.environ['environ'] = float(rain_fall)
    end_time = time_date.hour + ':' + time_date.minute + ':' + time_date.second 
    logger(start_time,end_time,rain_fall,pool_level,None,"-","-")

def outfall_detection(bravo_xbee,lcd,led_matrix):
  os.environ['status'] = None
  os.environ['restart'] = '0'
  if 'invoke' not in os.environ:
    os.environ['invoke'] = '0'
  while True:
    outfall = ""
    os.environ['status'] = str(checkmonth_sample())
    if os.environ['status'] == '1':
      while calculate_sleep('complete'):
        if check_restart():
          restart_state()
        pass
    elif os.environ['status'] == '0':
      while calculate_sleep('missed'):
        if check_restart():
          restart_state()
        pass
    elif os.environ['status'] == None:
      outfall = bravo_xbee.receive_message()
      if outfall == 'out':
        time_date = datetime.datetime.now()
        restart_date = time_date.month+'/'+time_date.year
        if os.environ['restart'] == '1' and restart_date == os.environ['invoke_date']:
          invoke_system(led_matrix,lcd,bravo_xbee)
        elif os.environ['invoke'] == '0' and os.environ['restart'] == '0':
          invoke_system(led_matrix, lcd, bravo_xbee)
