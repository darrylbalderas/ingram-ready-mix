'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This program was written to implement a alarm system in 
conjunction with the outfall detection system for the ingram 
ready mix plant
'''
import sys
import os
import RPi.GPIO as gpio
import glob
import serial
from time import time
import datetime
from calendar import monthrange
from time import sleep 
from math import floor

################ Global Variables #####################

global RESTART_HOLD 
RESTART_HOLD = 3 
# text file names used to hold values for enviroment variables 
# implementation
STATUS = './config_files/status_value.txt'
RAIN = './config_files/rain_value.txt'
POOL_LEVEL = './config_files/pool_level_value.txt'
RESTART = './config_files/restart_value.txt'
RESTART_DATE = './config_files/restart_date.txt'
RESTART_TIME = './config_files/restart_time.txt'
VOLTAGE = './config_files/voltage_value.txt'
INVOKE = './config_files/invoke_value.txt'
INVOKE_DATE = './config_files/invoke_date.txt'
INVOKE_TIME = './config_files/invoke_time.txt'
PINGS = './config_files/pings.txt'

# Datastructure that contains months
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

#Operation hours for the ingram ready mix facility
start_shift = 6
end_shift  = 24 # change back to 17
first_work_day = 0
last_work_day = 8 # change back to 5

# Data structure that contains of the pins used for the system
pin_dictionary = {'buzzers' : [4,17,27,22,6,13]
                , 'complete': 12
                , 'mute': 16
                , 'restart': 21
                , 'miss': 20}

################ GPIO Functions #####################
gpio.setmode(gpio.BCM)
gpio.setup(pin_dictionary['complete'],gpio.IN)
gpio.setup(pin_dictionary['mute'],gpio.IN)
gpio.setup(pin_dictionary['miss'],gpio.IN)
gpio.setup(pin_dictionary['restart'],gpio.IN)

def initalize_buzzers():
  '''
  Parameters: None
  Function: Initializes the pins used by the buzzers as output
  Returns: None
  '''
  for buzzer in pin_dictionary['buzzers']:
    gpio.setup(buzzer,gpio.OUT)

def check_complete():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for complete button has
  been pressed resulting in the status either a 1 or 0
  Returns: The status of the complete button
  '''
  return gpio.input(pin_dictionary['complete'])

def check_miss():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for miss button has been 
  pressed resulting in the status either a 1 or 0
  Returns: The status of the missed button
  '''
  return gpio.input(pin_dictionary['miss'])

def check_mute():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for mute button has been
  pressed resulting in the status either a 1 or 0
  Returns: The status of the mute button
  '''
  return gpio.input(pin_dictionary['mute'])

def check_restart():
  '''
  Parameter: None
  Function: Checks whether the gpio pin for restart button has been
  pressed resulting in the status either a 1 or 0
  Returns: The status of the restart button
  '''
  return gpio.input(pin_dictionary['restart'])

def start_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending
  a boolean value True in order to turn on
  Returns: None
  '''
  for buzzer in pin_dictionary['buzzers']:
    gpio.output(buzzer,True)

def stop_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending 
  a boolean value False in order to turn off
  Returns: None
  '''
  for buzzer in pin_dictionary['buzzers']:
    gpio.output(buzzer,False)

################ Helper Functions ###################

def get_pins():
  '''
  Paramters: None
  Function: used as a getter in order to access the data structure that has 
  the pin numberings
  Returns: Pin numbering dictionary
  '''
  return pin_dictionary

def remove_character(message,character):
  '''
  Parameters: string, string
  Function: Remove desired character from the message
  Returns: Message without the character in the parameters
  '''
  return message.strip(character)

def empty_queue(q):
  '''
  Parameters: a list (passed by reference)
  Function: Empty the list
  Returns: None 
  '''
  while len(q) != 0:
    q.pop(0)

def initialize_files():
  '''
  Parameters: None
  Function: Initialize files with default values if they have not been created
  Returns: None
  '''
  files = {'status':STATUS,
           'rain': RAIN,
           'pool_level': POOL_LEVEL,
           'restart' : RESTART,
           'restart_date': RESTART_DATE,
           'restart_time': RESTART_TIME,
           'voltage' : VOLTAGE,
           'invoke': INVOKE,
           'invoke_date': INVOKE_DATE,
           'invoke_time': INVOKE_TIME,
           'ping':PINGS
          }

  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')
  for key,value in files.items():
    if not os.path.exists(value):
      fopen = open(value, 'w')
      if key == 'invoke':
        fopen.write('0')
      elif key == 'rain':
        fopen.write('0.0')
      elif key == "pool_level":
        fopen.write('12.0')
      elif key == 'restart':
        fopen.write('0')
      elif key == 'restart_date':
        fopen.write('None')
      elif key == 'restart_time':
        fopen.write('None')
      elif key == 'voltage':
        fopen.write('12.0')
      elif key == 'invoke_date':
        fopen.write('None')
      elif key == 'invoke_time':
        fopen.write('None')
      elif key == 'ping ':
        fopen.write('0')
      else:
        fopen.write('-1')
      fopen.close()

def check_value_file(file_name):
  '''
  Paramter: file name (string)
  Function: Reads the value in the text file
  Returns: value in text file
  '''
  if os.path.exists(file_name):
    fopen = open(file_name,'r')
    tmp = fopen.read()
    return tmp
  else:
    return None

def set_value_file(file_name, value):
  '''
  Paramter: file name(string), value to set in text file
  Function: changes the value in the file name given
  Returns: None
  '''
  if os.path.exists(file_name):
    fopen = open(file_name,'w')
    fopen.write(value)
    fopen.close()
  else:
    return None

def lcd_serial_port():
  '''
  Paramter: None
  Function: Looks for the port used by the 16x2 LCD screen
  Returns: port used 16x2 screen port
  '''
  port =  glob.glob('/dev/ttyACM*')
  if len(port) != 0:
    return port[0]
  else:
    return None

def xbee_usb_port():
  '''
  Paramter: None
  Function: Looks for the port used by the XBee 
  Returns: port used by XBee
  '''
  if sys.platform.startswith('linux'):
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

def calculate_days():
  '''
  Paramter: None
  Function: Calculates the amount days left in a given month
  Returns: Days left in the month
  '''
  time_date = datetime.datetime.now()
  month, days_left = monthrange(time_date.year,time_date.month)
  return (days_left - time_date.day)

def calculate_hours():
  '''
  Paramter: None
  Function: Calculates the amount of hours left in the day
  Returns: hours left until the next day
  '''
  time_date = datetime.datetime.now()
  return (24 - time_date.hour)

def check_operation_hours(time_date):
  '''
  Paramter: (current time) 
  Function: Checks whether the current time is with the range of operation times
  Returns: True if within the range of operation hours (6am-5pm) otherwise False
  '''
  current_hour = time_date.hour
  current_min = time_date.minute
  working_hours = False
  if current_hour >= start_shift and current_hour < end_shift:
    if current_hour == (end_shift-1) and current_min > 58:
      working_hours = False
    else:
      working_hours = True
  else:
    working_hours = False
  return working_hours

def check_operation_days(time_date):
  '''
  Paramter: (current day)
  Function: Checks whether the current day is with the range of operation days
  Returns: True if within operation days ( monday - friday) otherwise False
  '''
  working_days = False
  if time_date.weekday() >= first_work_day and time_date.weekday() < last_work_day:
    working_days = True
  return working_days

def check_end_day():
  '''
  Paramter: None
  Function: Checks for the end of day to reset the values in rain and pool level text files 
  Returns: None
  '''
  time_date = datetime.datetime.now()
  if time_date.hour == 23 and time_date.minute == 59:
    set_value_file(RAIN,'0.0')
    set_value_file(POOL_LEVEL,'12.0')
    set_value_file(PINGS,'0')
    set_value_file(INVOKE_TIME,'None')
    set_value_file(RESTART_TIME,'None')
    set_value_file(INVOKE_DATE,'None')
    set_value_file(RESTART_DATE,'None')

def logger(start_time, end_time, amount_rain, pool_level, tag, outfall, status, operation):
  '''
  Paramter: start time( string), end time( string), the amount of rainfall( float), pool level( float), 
            tag( C, M, or None), outfall( Yes or No), collection status( complete, or missed) , 
            and operation hours(Yes or No)
  Function: Creates a directory for the log file to be populated with given parameters.
  Returns: None
  '''
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
  old_file = month_directory + file_name + '.ods'
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
      files = glob.glob(month_directory + file_name + '*.ods')
      if len(files) != 0:
        collect_datafile = files[0]
        command = "cp %s %s"%(old_file,collect_datafile)
        command2 = "rm %s"%(old_file)
        os.system(command)
        os.system(command2)
      else:
        collect_datafile = old_file
    fopen = open(collect_datafile,'a')
  else:
    if tag == 'C':
      collect_datafile = month_directory + file_name + '_completed.ods'
    elif tag == 'M':
      collect_datafile = month_directory + file_name + '_missed.ods'
    else:
      files = glob.glob(month_directory + file_name + '*.ods')
      if len(files) != 0:
        collect_datafile = files[0]
        command = "cp %s %s"%(old_file,collect_datafile)
        command2 = "rm %s"%(old_file)
        os.system(command)
        os.system(command2)
      else:
        collect_datafile = old_file
    fopen = open(collect_datafile, 'w')
    fopen.write('Start time, End time, Inches of Rain, Inches till Overflow,\
 Outfall status, Collection Status, Hours of Operation')
    fopen.write('\n')

  fopen.write("{},{},{},{},{},{},{}".format(start_time, end_time, amount_rain 
                                         ,pool_level, outfall, status, operation))
  fopen.write("\n")
  fopen.close()

################ Rainfall Thread Functions ############
def receive_voltage(voltage_queue,Locks):
  '''
  Paramter: voltage_queue( list for voltages)
  Function: Checks the list if voltage has been recieved. If voltage is received,
  Updates voltage file with received voltage
  Returns: None
 '''
  message = ""
  if len(voltage_queue) != 0:
    message = voltage_queue.pop(0)
    if len(message)  >= 3:
      if message[0] == 'v':
        voltage_val = remove_character(message,'v')
        Locks['voltage'].acquire()
        set_value_file(VOLTAGE,'%.2f'%(float(voltage_val)))
        Locks['voltage'].release()

def send_confirmation(trigger_queue,sender_queue,voltage_queue,Locks):
  '''
  Paramter: trigger_queue (list for rain guage triggers), sender_queue (list for 
  sending information), and voltage_queue( list for voltages)
  Function: Waiting for triggers and voltages. If trigger is recieved then it will 
  append a confirmation message in the sender queue.
  Returns:  None 
  '''
  message = ""
  flag = False
  while not flag:
    receive_voltage(voltage_queue, Locks)
    while len(trigger_queue) != 0:
      message = trigger_queue.pop(0)
      if message == "tri":
        print(message)
        sender_queue.append("tyes")
        sleep(0.5)
        sender_queue.append('tyes')
        flag = True
        break
    sleep(2)

def receive_data(rain_queue,sender_queue,voltage_queue,Locks):
  '''
  Paramter: rain_queue (list for rain and pool level data), sender_queue (list for 
  sending information), and voltage_queue ( list for voltages)
  Function: Waiting for rainfall and pool level data. If they have both been received then it will 
  append a confirmation message in sender queue. Update rainfall and pool level files with received
  values
  Returns: a tuple containing (rainfall and pool level)
  '''
  rain_flag = False
  pool_flag = False
  rain_val = 0
  pool_val = 0
  message = ""
  while not (rain_flag and pool_flag):
    if len(rain_queue) != 0:
      message = rain_queue.pop(0)
      if message[0] == 'r' and not rain_flag:
        rain_val = remove_character(message,'r')
        rain_flag = True
      elif message[0] == 'p'and not pool_flag:
        pool_val = remove_character(message,'p')
        pool_flag = True
  sender_queue.append("ryes")
  sleep(0.5)
  sender_queue.append('ryes')
  Locks['data'].acquire()
  set_value_file(RAIN,'%.2f'%(float(rain_val)))
  set_value_file(POOL_LEVEL,'%.2f'%(float(pool_val)))
  Locks['data'].release()
  print('got data')
  return (rain_val, pool_val)

################ Outfall thread Functions ##############

def check_low_voltage(voltage_level):
  '''
  Paramter: voltage level(string)
  Function: Checks if voltage level is below a certain threshold
  Returns: True if voltage is below the threshold otherwise False
  '''
  try:
    if float(voltage_level) >= 11.6 and float(voltage_level) < 16.0:
      return False
    else:
      return True
  except:
    return False

def send_outfall_conf(out_queue,sender_queue,lcd,led_matrix,Locks):
  '''
  Paramter: out_queue (list for flow sensor triggers), sender_queue( list for sending information),
  lcd (object), led_medtrix (object)
  Function: Waiting for outfall trigger from the flow sensor and level sensor and
  displaying the voltage level. Check voltage file if voltage level is below a certain threshold. If it is 
  below the threshold then the system will visually alert the user via the led matrix
  Returns: None
  '''
  message = ""
  flag = False
  voltage_level = ""
  low_voltage_flag = False
  lcd_clear_flag = False
  lcd.send_command("CLEAR")
  while not flag:
    Locks['voltage'].acquire()
    voltage_level = check_value_file(VOLTAGE)
    Locks['voltage'].release()
    tmp = voltage_level.split('.')
    tmp[0] = tmp[0].zfill(2)
    string_voltage_level = '.'.join(tmp)
    lcd.display_voltage(string_voltage_level,'None','None',low_voltage_flag)
    check_end_day()
    if check_low_voltage(voltage_level) == True:
      led_matrix.change_color(led_matrix.get_blueImage())
      low_voltage_flag = True
      if lcd_clear_flag == True:
        lcd.send_command("CLEAR")
        lcd_clear_flag = False
    else:
      low_voltage_flag = False
      led_matrix.change_color(led_matrix.get_greenImage())
      if lcd_clear_flag == False:
        lcd.send_command("CLEAR")
        lcd_clear_flag = True
    if check_restart():
      restart(lcd,led_matrix)
    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        lcd.send_command("CLEAR")
        sender_queue.append("oyes")
        sleep(0.5)
        sender_queue.append("oyes")
        flag = True
        break

def stop_outfall(out_queue,sender_queue,status,lcd,led_matrix,Locks):
  '''
  Paramter: out_queue (list for flow sensor triggers), sender_queue (list for sending information), 
  status( complete or missed), lcd (object), and led_matrix ( object)
  Waiting for outfall trigger from the flow sensor and level sensor and
  displaying the voltage level. Check voltage file if voltage level is below a certain threshold. If it is 
  below the threshold then the system will visually alert the user via the led matrix
  Returns: None
  '''
  message = ""
  flag = False
  voltage_level = ""
  low_voltage_flag = False
  lcd_clear_flag = False
  time_left = 0
  while not flag:
    Locks['voltage'].acquire()
    voltage_level = check_value_file(VOLTAGE)
    Locks['voltage'].release()
    tmp = voltage_level.split('.')
    tmp[0] = tmp[0].zfill(2)
    string_voltage_level = '.'.join(tmp)
    if status == "complete":
      time_left = calculate_days()
    elif status == "missed":
      time_left = calculate_hours()
    lcd.display_voltage(string_voltage_level,time_left,status,low_voltage_flag)
    check_end_day()
    if check_restart():
      restart(lcd,led_matrix)

    if check_low_voltage(voltage_level) == True:
      low_voltage_flag = True
      led_matrix.change_color(led_matrix.get_blueImage())
      if lcd_clear_flag == True:
        lcd.send_command("CLEAR")
        lcd_clear_flag = False
    else:
      low_voltage_flag = False
      if status == 'complete':
        led_matrix.change_color(led_matrix.get_greenImage())
      elif status == 'missed':
        led_matrix.change_color(led_matrix.get_redImage())

      if lcd_clear_flag == False:
        lcd.send_command("CLEAR")
        lcd_clear_flag = True

    if check_sleep(status) == False:
      lcd.send_command("CLEAR")
      flag = True

    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        sender_queue.append("oyes")
        sleep(0.5)
        sender_queue.append("oyes")
        flag = True
        break

def restart(lcd,led_matrix):
  '''
  Paramter: lcd (object), led_matrix(objec), current_time(float)
  Function: Display count down timer in 16x2 lcd screen for holding
  the restart button.If the user has succesfully hold the restart
  button for 3 seconds then the system will restart otherwise it break 
  from this function.
  Returns: None
  '''
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
  os.system("sudo reboot")

def invoke_system(led_matrix,lcd, collection_time,Locks):
  '''
  Paramter: led_matrix (object), lcd(object), collection_time(float)
  Function: Invoke buzzers, create collection time timer on 16x2 lcd, 
  and change led matrix color. Each column in the led matrix represents a 
  column minute. Led matrix will change color by column until it reaches the 15
  minute limited. Between those 15 minutes, checking of the buttons is done to 
  see if they want to complete or miss sample, restart the system and 
  mute the buzzers
  Returns: None
  '''
  start_buzzer()
  blinking_delay = 0.5 #seconds
  time_date = datetime.datetime.now()
  start_time = '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  set_value_file(INVOKE, '1')
  set_value_file(INVOKE_DATE,'%s/%s/%s'%(time_date.month,time_date.day,time_date.year))
  set_value_file(INVOKE_TIME,start_time)
  led_matrix.make_blink(led_matrix.get_yellowImage(), blinking_delay)
  begin_time = time()-(900-collection_time)
  while (time()-begin_time) <= led_matrix.get_collection_time():
    if check_complete():
      led_matrix.change_color(led_matrix.get_greenImage())
      lcd.complete_message()
      complete_state(led_matrix,start_time,Locks)
      break
    elif check_mute():
      stop_buzzer()
    elif check_restart():
      restart_state(lcd,led_matrix,start_time,time_date)
      break
    elif check_miss():
      led_matrix.change_color(led_matrix.get_redImage())
      lcd.missed_message()
      missed_state(led_matrix,start_time,Locks)
      break
    led_matrix.make_blink(led_matrix.get_yellowImage(),blinking_delay)
    led_matrix.change_color(led_matrix.get_yellowImage())
    lcd.display_timer(time()-begin_time)
  if (time()-begin_time) > collection_time:
    led_matrix.change_color(led_matrix.get_redImage())
    lcd.missed_message()
    missed_state(led_matrix,start_time,Locks)
  stop_buzzer()

def complete_state(led_matrix,start_time,Locks):
  '''
  Paramter: led matrix(object), start_time(string)
  Function: stops the buzzers and changes led_matrix to green and Logs data 
  Returns: None
  '''
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_greenImage())
  outfall = 'Yes'
  Locks['data'].acquire()
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  Locks['data'].release()
  status = "completed"
  operation = "Yes"
  time_date = datetime.datetime.now()
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  Locks['logger'].acquire()
  logger(start_time, end_time, amount_rain, pool_level, 'C', outfall, status,operation)
  Locks['logger'].release()
  set_value_file(INVOKE,'0')
  set_value_file(INVOKE_DATE, 'None')
  set_value_file(INVOKE_TIME,'None')
  set_value_file(RESTART,'0')
  set_value_file(RESTART_TIME,'None')
  set_value_file(RESTART_DATE,'None')

def missed_state(led_matrix,start_time,Locks):
  '''
  Paramter: led matrix(object), start_time(string)
  Function: stops the buzzers and changes led_matrix to red and Logs data 
  Returns: None
  '''
  stop_buzzer()
  led_matrix.clear_matrix()
  led_matrix.change_color(led_matrix.get_redImage())
  outfall = 'Yes'
  Locks['data'].acquire()
  pool_level = check_value_file(POOL_LEVEL)
  amount_rain = check_value_file(RAIN)
  Locks['data'].release()
  status = "missed"  
  operation = "Yes"
  time_date = datetime.datetime.now() 
  end_time =  '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
  Locks['logger'].acquire()
  logger(start_time, end_time ,amount_rain, pool_level, 'M', outfall, status,operation)
  Locks['logger'].release()
  set_value_file(INVOKE,'0')
  set_value_file(INVOKE_DATE, 'None')
  set_value_file(INVOKE_TIME,'None')
  set_value_file(RESTART,'0')
  set_value_file(RESTART_TIME,'None')
  set_value_file(RESTART_DATE,'None')

def restart_state(lcd,led_matrix,start_time,time_date):
  '''
  Paramter: lcd (object), led_matrix(objec)
  Function: Display count down timer in 16x2 lcd screen for holding
  the restart button.If the user has succesfully hold the restart
  button for 3 seconds then the system will restart otherwise it break 
  from this function.
  Returns: None
  '''
  lcd.send_command('CLEAR')
  state = 0
  end_time = 0
  begin_time = time()
  while end_time < RESTART_HOLD:
    end_time = time() - begin_time
    lcd.holding_restart(end_time)
    state = check_restart()
    if not state:
      return
  stop_buzzer()
  lcd.restart_message()
  led_matrix.clear_matrix()
  set_value_file(RESTART,'1')
  set_value_file(RESTART_TIME,start_time)
  set_value_file(RESTART_DATE,'%s/%s/%s'%(time_date.month,time_date.day,time_date.year))
  print('restart')
  # os.system("sudo reboot")

def check_time(new_time_string, old_time_string):
  '''
  time_string.split(':')
  position 0 in time_string: hours
  position 1 in time_string: minutes
  position 2 in time_string: seconds
  '''
  if new_time_string == 'None' or old_time_string == 'None':
    return 0
  else:
    new_time = [int(value) for value in new_time_string.split(':')]
    old_time = [int(value) for value in old_time_string.split(':')]
    if new_time[0] == 0 and old_time[0] == 23:
      new_time[0] = 24
    hour = new_time[0] - old_time[0]
    minute = new_time[1] - old_time[1]
    second = new_time[2] - old_time[2]
    total_time = (hour*3600) + (minute*60) + second
    if total_time >= 900:
      return 0
    else:
      if (900-total_time) > 5:
        return 900-total_time
      else:
        return 0

def checkmonth_sample():
  '''
  Paramter: None 
  Function: Checks if there are any missed or complete 
  files within the log files for the month. 
  Returns: 1 for complete files, 0 for missed files, and -1 if there is no missed
  or complete files
  '''
  time_date = datetime.datetime.now()
  complete_dir = '/home/pi/Desktop/log_data/%s/%s/*completed.ods'%(time_date.year,months[str(time_date.month)])
  missed_dir = '/home/pi/Desktop/log_data/%s/%s/*missed.ods'%(time_date.year, months[str(time_date.month)])
  complete_files = glob.glob(complete_dir)
  miss_files = glob.glob(missed_dir)
  if len(complete_files) > 0:
    set_value_file(STATUS,'1')
  elif len(miss_files) > 0:
    set_value_file(STATUS,'0')
  else:
    set_value_file(STATUS,'-1')

def check_sleep(status):
  '''
  Paramter: status(missed or complete)
  Function: checks how much time sleep time is left 
  for the given status. The complete status checks how many 
  days there is left in the month. The missed status checks how many hours are left 
  in the day. 
  Returns: True if there is still time left for the given status otherwise
  false
  '''
  if status == 'missed' and calculate_hours() > 0:
    return True
  elif status == 'complete' and calculate_days() > 0:
    return True
  return False
  
################ Thread Functions ########################
def rain_detection(trigger_queue,rain_queue,voltage_queue,sender_queue, Locks):
  '''
  Paramter: trigger_queue (list for rain guage triggers), rain_queue ( list for rainfall and pool
  level data), voltage_queue (list for voltage), sender_queue (list for sending information),
  event ( Thread flag)
  Function: Checking for triggers by the rain guage on the rainfall detection system. If triggered
  then sends confirmation waiting for rainfall and pool level. If data received then sends a 
  confirmation for receiving the data and updates rainfall and pool level text files. 
  Also checks for receiving the voltage and updates the voltage text files
  Returns: 
  '''
  while True:
    send_confirmation(trigger_queue,sender_queue,voltage_queue,Locks)
    start_timeDate = datetime.datetime.now()
    rain_fall, pool_level = receive_data(rain_queue,sender_queue,voltage_queue,Locks)
    end_timeDate = datetime.datetime.now()  
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    if check_operation_hours(start_timeDate) and check_operation_days(start_timeDate):
      operation = "Yes"
    else:
      operation = "No"
    Locks['logger'].acquire()
    logger(start_time, end_time, rain_fall, pool_level, None ,"  -  ","  -  ",operation)
    Locks['logger'].release()
    print('log the data')

def outfall_detection(lcd,led_matrix,out_queue,sender_queue,Locks):
  '''
  Paramter: lcd (object), led_matrix(object), out_queue( list for 
  flow sensor triqqers), sender_queue (list for sending information), 
  event (Thread flag)
  Function: Check if there is outfall occuring and consider if the user 
  has collected or missed the sample.
  Returns: None
  '''
  set_value_file(STATUS,'-1')
  while True:
    collection_time = 900
    checkmonth_sample()
    if check_value_file(STATUS) == '1':
      stop_outfall(out_queue,sender_queue,'complete',lcd,led_matrix,Locks)
    elif check_value_file(STATUS) == '0':
      stop_outfall(out_queue,sender_queue,'missed',lcd,led_matrix,Locks)
    elif check_value_file(STATUS) == '-1':
      time_date = datetime.datetime.now()
      restart_date = '%s/%s/%s'%(time_date.month,time_date.day,time_date.year)
      restart_time = '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
      if check_value_file(RESTART) == '1' and restart_date == check_value_file(RESTART_DATE):
        collection_time = check_time(restart_time,check_value_file(RESTART_TIME))
        if collection_time > 0:
          if check_operation_hours(time_date) and check_operation_days(time_date):
            set_value_file(RESTART,'0')
            set_value_file(RESTART_DATE,'None')
            set_value_file(RESTART_TIME,'None')
            invoke_system(led_matrix,lcd,collection_time,Locks)
          else:
            set_value_file(RESTART,'0')
            set_value_file(RESTART_DATE,'None')
            set_value_file(RESTART_TIME,'None')
        else:
            set_value_file(RESTART,'0')
            set_value_file(RESTART_DATE,'None')
            set_value_file(RESTART_TIME,'None')

      else:
        time_date = datetime.datetime.now()
        invoke_date = '%s/%s/%s'%(time_date.month,time_date.day,time_date.year)
        invoke_time = '%s:%s:%s'%(time_date.hour,time_date.minute,time_date.second)
        if check_value_file(INVOKE) == '1' and invoke_date == check_value_file(INVOKE_DATE):
          collection_time = check_time(invoke_time,check_value_file(INVOKE_TIME))
          if collection_time > 0:
            if check_operation_hours(time_date) and check_operation_days(time_date):
              invoke_system(led_matrix,lcd,collection_time,Locks)
            else:
              set_value_file(INVOKE,'0')
              set_value_file(INVOKE_DATE,'None')
              set_value_file(INVOKE_TIME,'None')
          else:
              set_value_file(INVOKE,'0')
              set_value_file(INVOKE_DATE,'None')
              set_value_file(INVOKE_TIME,'None')
        elif check_value_file(INVOKE) == '0':
          empty_queue(out_queue)    #move under the elif statement 
          lcd.send_command('CLEAR')
          send_outfall_conf(out_queue,sender_queue,lcd,led_matrix,Locks) #might need to change function to waiting_outfall
          time_date = datetime.datetime.now()
          if check_operation_hours(time_date) and check_operation_days(time_date):
            collection_time = led_matrix.get_collection_time()
            invoke_system(led_matrix,lcd,collection_time,Locks)
          else:
            Locks['data'].acquire()
            rain = check_value_file(RAIN)
            level = check_value_file(POOL_LEVEL)
            Locks['data'].release()
            operation = "No"
            outfall = "Yes"
            collection_status = "missed"
            Locks['logger'].acquire()
            logger("  -  ","  -  ", rain,level, None, outfall ,collection_status, operation)
            Locks['logger'].release()

def transmission(xbee):
  '''
  Paramter: xbee(object) event( Thread flag)
  Function: sends messages in the send_queue and receieves messages and
  places in there respect queue
  Returns: None
  '''
  switch_flag = False
  while True:
    if switch_flag == False:
      xbee.receive_message()
      switch_flag = True
    else:
      xbee.send_message()
      switch_flag = False
