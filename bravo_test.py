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
VOLTAGE = './config_files/voltage_val.txt'
COLLECTION_TIME = './config_files/collection_time.txt'

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

start_shift = 6
end_shift  = 17

buzzers = [4,17,22,27,5,6,13,19] 
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
  files = {'status':STATUS,
           'invoke': INVOKE,
           'invoke_date': INVOKE_DATE,
           'rain': RAIN,
           'pool_level': POOL_LEVEL,
           'restart' : RESTART,
           'voltage' : VOLTAGE,
           'collection_time': COLLECTION_TIME
          }
  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')

  for key,value in files.items():
    if os.path.exists(value):
      fopen = open(value, 'w')
      if key == 'invoke':
        fopen.write('0')
      elif key == 'rain':
        fopen.write('2.769')
      elif key == "pool_level":
        fopen.write('8.0')
      elif key == 'restart':
        fopen.write('0')
      elif key == 'invoke_date':
        fopen.write('None')
      elif key == 'voltage':
        fopen.write('12.0')
      elif key == 'collection_time':
        fopen.write('900')
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

def logger(start_time, end_time, amount_rain, pool_level, tag, outfall, status, operation):
  time_date = datetime.datetime.now()
  old_file = ""
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

  old_file = month_directory + file_name+'.ods'
  if os.path.exists(old_file):
    if tag == 'C':
      collect_datafile = month_directory + file_name+'_completed.ods'
      command = "cp %s %s"%(old_file,collect_datafile)
      command2 = "rm %s"%(old_file)
      os.system(command)
      os.system(command2)
    elif tag == 'M':
      collect_datafile = month_directory + file_name+'_missed.ods'
      command = "cp %s %s"%(old_file,collect_datafile)
      command2 = "rm %s"%(old_file)
      os.system(command)
      os.system(command2)
    else:
      collect_datafile = old_file

    fopen = open(collect_datafile,'a')
  else:
    if tag == 'C':
      collect_datafile = month_directory + file_name+'_completed.ods'
    elif tag == 'M':
      collect_datafile = month_directory + file_name+'_missed.ods'
    else:
      collect_datafile = old_file
    fopen = open(collect_datafile, 'w')
    fopen.write('Start time, End time, AmountRained(inches), Inches till Overflow, \
                 Outfall status, Collection Status','Hours of Operation')
    fopen.write('\n')

  fopen.write("{},{},{},{},{},{},{}".format(start_time, end_time, amount_rain 
                                         ,pool_level, outfall, status, operation))
  fopen.write("\n")
  fopen.close()

def invoke_system(led_matrix,lcd, collection_time):
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
  row_duration = collection_time/float(8)
  while current_time <= collection_time:
    if check_complete():
      lcd.complete_message()
      complete_state(led_matrix,start_time)
      break
    elif check_mute():
      stop_buzzer()
    elif check_restart():
      restart_state(lcd,led_matrix,collection_time-current_time)
    elif check_miss():
      lcd.missed_message()
      missed_state(led_matrix,start_time)
      break

    current_time = time() - timer
    lcd.display_timer(collection_time-current_time)
    if current_time >= row_duration * count_row:
          led_matrix.change_color_row(invoke_color,led_matrix.get_red(),count_row)
          count_row += 1
  if count_row >= 8: 
    lcd.missed_message()
    missed_state(led_matrix,start_time)
  else:
    stop_buzzer()
    led_matrix.change_color(led_matrix.get_greenImage())

  set_value_file(COLLECTION_TIME,'900')
 
def complete_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  status = "completed"
  operation = "Yes"
  time_date = datetime.datetime.now()
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  logger(start_time, end_time, amount_rain, pool_level, 'C', outfall, status,operation)
  set_value_file(INVOKE,'0')
  set_value_file(RESTART,'0')

def missed_state(led_matrix,start_time):
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  status = "missed"  
  operation = "Yes"
  time_date = datetime.datetime.now() 
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  logger(start_time, end_time ,amount_rain, pool_level, 'M', outfall, status,operation)
  set_value_file(INVOKE,'0')
  set_value_file(RESTART,'0')
  
def restart_state(lcd,led_matrix,current_time):
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
  set_value_file(COLLECTION_TIME,current_time)
  set_value_file(RESTART, '1')
  os.system("sudo reboot")

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

def transmission(xbee):
  while True:
      xbee.receive_message()
      xbee.send_message()

def remove_character(message,character):
  return message.strip(character)

def send_confirmation(trigger_queue,sender_queue):
  message = ""
  flag = False
  while not flag:
    while len(trigger_queue) != 0:
      message = trigger_queue.pop(0)
      if message == "tri":
        sender_queue.append("tyes")
        flag = True
        break

def receive_data(rain_queue,sender_queue):
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    if len(rain_queue) != 0:
      message = rain_queue.pop(0)
      if message != "out" or message != "tri":
        if message[0] == 'r' and not rain_flag:
          rain_val = remove_character(message,'r')
          rain_flag = True
        elif message[0] == 'p'and not pool_flag:
          pool_val = remove_character(message,'p')
          pool_flag = True
  sender_queue.append("ryes")
  set_value_file(RAIN,rain_val)
  set_value_file(POOL_LEVEL,pool_val)
  return (rain_val, pool_val)

def rain_detection(trigger_queue,rain_queue,sender_queue):
  while True:
    send_confirmation(trigger_queue,sender_queue)
    start_timeDate = datetime.datetime.now()
    rain_fall, pool_level = receive_data(rain_queue,sender_queue)
    end_timeDate = datetime.datetime.now()  
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    if check_operation_hours(start_timeDate) and check_operation_days(start_timeDate):
      operation = "Yes"
    else:
      operation = "No"
    logger(start_time, end_time, rain_fall, pool_level, None ,"  -  ","  -  ",operation)



def check_operation_hours(time_date):
  current_hour = time_date.hour
  current_min = time_date.minute
  working_hours = False
  if current_hour >= start_shift and current_hour <= end_shift:
    if current_hour == end_shift and current_min > 0:
      working_hours = False
    else:
      working_hours = True
  return working_hours

def check_operation_days(time_date):
  working_days = False
  if time_date.weekday()>= 0 and time_date.weekday() < 5:
    working_days = True
  return working_days

def check_end_day():
  time_date = datetime.datetime.now()
  if time_date.hour == 24:
    set_value_file(RAIN,'2.769')
    set_value_file(POOL_LEVEL,'8.0')

def empty_queue(q):
  while len(q) != 0:
    q.pop(0)

def send_outfall_conf(out_queue,sender_queue,lcd,led_matrix):
  message = ""
  flag = False
  voltage_level = ""
  low_voltage_flag = False
  while not flag:
    voltage_level = check_value_file(VOLTAGE)

    if low_voltage_flag == True:
      lcd.low_voltage()
    else:
      lcd.display_voltage(voltage_level,'None','None')


    if check_low_voltage(voltage_level) == True:
      led_matrix.change_color(led_matrix.get_blueImage())
      low_voltage_flag = True
    else:
      low_voltage_flag = False
      led_matrix.change_color(led_matrix.get_blueImage())


    if check_restart():
      restart_state(lcd,led_matrix)


    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        lcd.send_command("CLEAR")
        sender_queue.append("oyes")
        flag = True
        break

def stop_outfall(out_queue,sender_queue,status,lcd,led_matrix):
  message = ""
  flag = False
  voltage_level = ""
  low_voltage_flag = False
  while not flag:
    voltage_level = check_value_file(VOLTAGE)
    if status == "complete":
      time_left = calculate_days()
    elif status == "missed":
      time_left = calculate_hours()

    if low_voltage_flag == True:
      lcd.low_voltage()
    else:
      lcd.display_voltage(voltage_level,time_left,status)

    if check_restart():
      restart_state(lcd,led_matrix)

    if check_low_voltage(voltage_level) == True:
      led_matrix.change_color(led_matrix.get_blueImage())
      low_voltage_flag = True
    else:
      low_voltage_flag = False
      led_matrix.change_color(led_matrix.get_greenImage())

    if check_sleep(status) == False:
      lcd.send_command("CLEAR")
      flag = True

    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        sender_queue.append("oyes")
        flag = True
        break

def outfall_detection(lcd,led_matrix,out_queue,sender_queue):
  set_value_file(STATUS,'-1')
  while True:
    collection_time = 900
    status = checkmonth_sample()
    set_value_file(STATUS,status)
    if check_value_file(STATUS) == '1':
      stop_outfall(out_queue,sender_queue,status,lcd,led_matrix)
    elif check_value_file(STATUS) == '0':
      stop_outfall(out_queue,sender_queue,status,lcd,led_matrix)
    elif check_value_file(STATUS) == '-1':
      empty_queue(out_queue)
      lcd.send_command('CLEAR')
      send_outfall_conf(out_queue,sender_queue,lcd,led_matrix)
      time_date = datetime.datetime.now()
      restart_date = '%s/%s'%(time_date.month,time_date.year)
      if check_value_file(RESTART) == '1' and restart_date == check_value_file(INVOKE_DATE):
        collection_time = int(check_value_file(COLLECTION_TIME))
        if collection_time >= 10:
          if check_operation_hours() and check_operation_days():
            invoke_system(led_matrix,lcd,collection_time)
          else:
            set_value_file(COLLECTION_TIME,'900')
      elif check_value_file(INVOKE) == '0':
        if check_operation_hours(time_date) and check_operation_days(time_date):
          collection_time = int(led_matrix.get_collection_time)
          invoke_system(led_matrix,lcd,collection_time)
        else:
          rain = check_value_file(RAIN)
          level = check_value_file(POOL_LEVEL)
          operation = "No"
          outfall = "Yes"
          collection_status = "missed"
          logger("  -  ","  -  ", rain,level, None, outfall ,collection_status, operation)


def check_low_voltage(voltage_level):
  if float(voltage_level) <= 6.0:
    return True
  else:
    return False

def get_voltageLevel(voltage_queue,send_queue):
  while True:
    send_voltage_conf(voltage_queue,send_queue)
    voltage_level = receive_voltage(voltage_queue,send_queue)
    set_value_file(VOLTAGE,voltage_level)

def send_voltage_conf(voltage_queue,send_queue):
  message = ""
  flag = False
  while not flag:
    while len(voltage_queue) != 0:
      message = voltage_queue.pop(0)
      if message == "vol":
        send_queue.append("vyes")
        flag = True
        break

def receive_voltage(voltage_queue,send_queue):
  voltage_flag = False
  voltage_val = 0
  message = ""
  while not voltage_flag:
    if len(voltage_queue) != 0:
      message = voltage_queue.pop(0)
      if message[0] == 'v' and not voltage_flag:
        voltage_val = remove_character(message,'v')
        voltage_flag = True
  send_queue.append("vyes")
  return voltage_val
