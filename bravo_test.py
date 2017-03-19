import sys
import os
import RPi.GPIO as gpio
import glob
import serial
from time import time
import datetime
from time import sleep 
from calendar import monthrange
# from transceiver import Transceiver
# from lcd import LCD
# from ledmatrix import LedMatrix
# from datetime import timedelta

global RESTART_HOLD 
RESTART_HOLD = 3 #seconds 

STATUS = './config_files/status_val.txt'
INVOKE = './config_files/invoke_val.txt'
INVOKE_DATE = './config_files/invoke_date_val.txt'
RAIN = './config_files/rain_val.txt'
POOL_LEVEL = './config_files/pool_level_val.txt'
RESTART = './config_files/restart_val.txt'

months = {'1': 'January',
          '2': 'February',
          '3': 'March',
          '4': 'April',
          '5': 'May',
          '6': 'June',
          '7': 'July',
          '8': 'August',
          '9': 'September',
          '10': 'October',
          '11': 'November',
          '12': 'December'
          }


## gpio pins used 
buzzers = [4,17,22,27,5,6,13,19] ## wiring in beardboard
complete = 12 
mute = 20
miss = 16
restart = 21
gpio.setmode(gpio.BCM)
gpio.setup(complete,gpio.IN)
gpio.setup(mute,gpio.IN)
gpio.setup(miss,gpio.IN)
gpio.setup(restart,gpio.IN)


def initialize_files():
  files = {'status': './config_files/status_val.txt',
           'invoke': './config_files/invoke_val.txt',
           'invoke_date': './config_files/invoke_date_val.txt',
           'rain': './rain_val.txt',
           'pool_level': './config_files/pool_level_val.txt',
           'restart' : './config_files/restart_val.txt'
          }
  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')

  for key,value in files.items():
    if os.path.exists(value):
      fopen = open(value, 'w')
      if key == 'invoke':
        fopen.write('0')
      elif key == 'rain':
        fopen.write('0.011')
      elif key == "pool_level":
        fopen.write('8')
      elif key == 'restart':
        fopen.write('0')
      elif key == 'invoke_date':
        fopen.write('None')
      else:
        fopen.write('-1')
      fopen.close()

def check_value_file(file_name):
  if os.path.exists(file_name):
    fopen = open(file_name,'r')
    tmp = fopen.read()
    return tmp
  else:
    return None

def set_value_file(file_name, value):
  if os.path.exists(file_name):
    fopen = open(file_name,'w')
    fopen.write(value)
    fopen.close()
  else:
    return None

def check_complete():
  return gpio.input(complete)

def check_miss():
  return gpio.input(miss)

def check_mute():
  return gpio.input(mute)

def check_restart():
  return gpio.input(restart)

def check_buttons():
  while True:
    print(check_complete())
    print(check_miss())
    print(check_mute())
    print(check_restart())
    print('\n\n')
    sleep(0.5)

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
  if len(port) != 0:
    return port[0]
  else:
    return None

def xbee_usb_port():
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
  if len(ports) != 0:
    result = []
    for port in ports:
        try:
            ser = serial.Serial(port)
            ser.close()
            result.append(port)
        except( OSError, serial.SerialException ):
            pass
    return result[0]
  else:
    return None

def logger(start_time, end_time, amount_rain, pool_level, tag=None, outfall=None, status=None):
  time_date = datetime.datetime.now()
  directory = '/home/pi/Desktop/log_data/'
  if not os.path.exists(directory):
    os.system('mkdir ' + directory)
  year_directory = directory + str(time_date.year) + '/'
  if not os.path.exists(year_directory):
    os.system('mkdir ' + year_directory)
  month_directory = year_directory + months[str(time_date.month)] + '/'
  if not os.path.exists(month_directory):
    os.system('mkdir ' + month_directory)
  file_name = '%s_%s_%s'%(time_date.month, time_date.day,time_date.year)
  if tag == 'C':
    collect_datafile = month_directory + file_name+'_completed.ods'
  elif tag == 'M':
    collect_datafile = month_directory + file_name+'_missed.ods'
  else:
    collect_datafile = month_directory + file_name+'.ods'

  if os.path.exists(collect_datafile):
    fopen = open(collect_datafile, 'a')
  else:
    fopen = open(collect_datafile, 'w')
    fopen.write('Start time, End time, AmountRained(inches), Inches till Overflow, \
                 Outfall status, Collection Status')
    fopen.write('\n')

  fopen.write("{},{},{},{},{},{}".format(start_time, end_time, amount_rain 
                                         ,pool_level, outfall, status))
  fopen.write("\n")
  fopen.close()

def invoke_system(led_matrix,lcd):
  time_date = datetime.datetime.now()
  start_time = '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  start_buzzer()
  invoke_date = '%s/%s'%(time_date.month,time_date.year)
  set_value_file(INVOKE_DATE,invoke_date)
  set_value_file(INVOKE, '1')
  count_row = 1
  invoke_color = led_matrix.ingram_colors("yellow")
  led_matrix.change_color(led_matrix.get_yellowImage())
  current_time = 0
  timer = time()
  while current_time <= led_matrix.get_max_time():
    if check_complete():
      lcd.complete_message()
      complete_state(led_matrix,start_time)
      return 
    if check_mute():
      stop_buzzer()
    if check_restart():
      restart_state(lcd,led_matrix)
    current_time = time() - timer
    lcd.display_timer(led_matrix.get_max_time()-current_time)
    if current_time >= led_matrix.get_row_duration()*count_row:
          led_matrix.change_color_row(invoke_color,led_matrix.get_red(),count_row)
          count_row += 1
  if count_row >= 8: 
    lcd.missed_message()
    missed_state(lcd,led_matrix,start_time)
  else:
    stop_buzzer()
    led_matrix.change_color(led_matrix.get_greenImage())
 
def complete_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  status = "completed"  
  time_date = datetime.datetime.now()
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  logger(start_time, end_time, amount_rain, pool_level, 'C', outfall, status)
  set_value_file(INVOKE,'0')
  set_value_file(RESTART,'0')

def missed_state(lcd,led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  status = "missed"  
  time_date = datetime.datetime.now() 
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  logger(start_time, end_time ,amount_rain, pool_level, 'M', outfall, status)
  set_value_file(INVOKE,'0')
  set_value_file(RESTART,'0')
  while not check_miss():
    lcd.pressed_missed()
  lcd.send_command("CLEAR")
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
  set_value_file(RESTART, '1')
  print("reset")  # for testing purposes
  # os.system("sudo reboot")

def checkmonth_sample():
  time_date = datetime.datetime.now()
  complete_dir = '/home/pi/Desktop/log_data/%s/%s/*completed.ods'%(time_date.year,months[str(time_date.month)])
  missed_dir = '/home/pi/Desktop/log_data/%s/%s/*missed.ods'%(time_date.year, months[str(time_date.month)])
  complete_files = glob.glob(complete_dir)
  miss_files = glob.glob(missed_dir)
  if len(complete_files) > 0:
    return '1'
  elif len(miss_files) > 0:
    return '0'
  else:
    return '-1'

def check_sleep(status):
  if status == 'missed' and calculate_hours() > 0:
    return True
  elif status == 'complete' and calculate_days() > 0:
    return True
  return False

def calculate_days():
  time_date = datetime.datetime.now()
  month, days_left = monthrange(time_date.year,time_date.month)
  return (days_left - time_date.day)

def calculate_hours():
  time_date = datetime.datetime.now()
  return (24 - time_date.hour)

def send_confirmation(xbee):
  message = ""
  while not message == 'tri':
      message = xbee.receive_message()
  xbee.send_message("tyes\n")
  sleep(0.5)

def receive_data(bravo_xbee):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    message = bravo_xbee.receive_message()
    if len(message) != 0:
      if message[0] == 'r' and not rain_flag:
        rain_val = bravo_xbee.remove_character(message,'r')
        set_value_file(RAIN,rain_val)
        rain_flag = True
      elif message[0] == 'p' and not pool_flag:
        pool_val = bravo_xbee.remove_character(message,'p')
        set_value_file(POOL_LEVEL,pool_val)
        pool_flag = True
    bravo_xbee.send_message("rno\n")
    sleep(0.5)
  bravo_xbee.send_message("ryes\n")
  sleep(0.5)
  return (rain_val, pool_val)

def rain_detection(bravo_xbee,lock,event):
  while not event.isSet():
    lock.acquire()
    send_confirmation(bravo_xbee)
    lock.release()
    start_timeDate = datetime.datetime.now()
    lock.acquire()
    send_confirmation(bravo_xbee)
    rain_fall, pool_level = receive_data(bravo_xbee)
    lock.release()
    end_timeDate = datetime.datetime.now() 
    # time_delay = datetime.datetime.now() - timedelta(minute = 5)  
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    logger(start_time, end_time, rain_fall, pool_level, None ,"  -  ","  -  ")

def send_outfall_conf(lcd, xbee):
  message = ""
  while not message == 'out':
    lcd.waiting_outfall()
    message = xbee.receive_message()
  xbee.send_message("oyes\n")
  sleep(0.5)

def outfall_detection(bravo_xbee,lcd,led_matrix,lock,event):
  set_value_file(STATUS,'-1')
  while not event.isSet():
    status = checkmonth_sample()
    set_value_file(STATUS,status)
    if status  == '1':
      while check_sleep('complete'):
        num_days = calculate_days()
        if check_restart():
          restart_state(lcd,led_matrix)
        lcd.display_days(num_days)
    elif status == '0':
      while check_sleep('missed'):
        num_hours = calculate_hours()
        if check_restart():
          restart_state(lcd,led_matrix)
        lcd.display_hour(num_hours)
    elif status == '-1':
      lock.acquire()
      send_outfall_conf(lcd,bravo_xbee)
      lock.release()
      time_date = datetime.datetime.now()
      restart_date = '%s/%s'%(time_date.month,time_date.year)
      if check_value_file(RESTART) == '1' and restart_date == check_value_file(INVOKE_DATE):
        invoke_system(led_matrix,lcd)
      elif check_value_file(INVOKE) == '0':
        invoke_system(led_matrix, lcd)
