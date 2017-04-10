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

################ Global Variables #####################

global RESTART_HOLD 
RESTART_HOLD = 3 
# text file names used to hold values for enviroment variables 
# implementation
STATUS = './config_files/status_val.txt'
INVOKE = './config_files/invoke_val.txt'
INVOKE_DATE = './config_files/invoke_date_val.txt'
RAIN = './config_files/rain_val.txt'
POOL_LEVEL = './config_files/pool_level_val.txt'
RESTART = './config_files/restart_val.txt'
VOLTAGE = './config_files/voltage_val.txt'
COLLECTION_TIME = './config_files/collection_time.txt'

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
end_shift  = 17

# Data structure that contains of the pins used for the system
pin_dictionary = {'buzzers' : [7,11,13,15,29,31,33,35]
                , 'complete': 32
                , 'mute': 36
                , 'restart': 38
                , 'miss': 40}


################ GPIO Functions #####################
gpio.setmode(gpio.BOARD)
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
        fopen.write('0.1690')
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
  if current_hour >= start_shift and current_hour <= end_shift:
    if current_hour == end_shift and current_min > 0:
      working_hours = False
    else:
      working_hours = True
  return working_hours

def check_operation_days(time_date):
  '''
  Paramter: (current day)
  Function: Checks whether the current day is with the range of operation days
  Returns: True if within operation days ( monday - friday) otherwise False
  '''
  working_days = False
  if time_date.weekday()>= 0 and time_date.weekday() < 5:
    working_days = True
  return working_days

def check_end_day():
  '''
  Paramter: None
  Function: Checks for the end of day to reset the values in rain and pool level text files 
  Returns: None
  '''
  time_date = datetime.datetime.now()
  if time_date.hour == 24:
    set_value_file(RAIN,'0.1690')
    set_value_file(POOL_LEVEL,'8.0')
    set_value_file(COLLECTION_TIME, '900')

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
    fopen.write('Start time, End time, AmountRained(cubic inches), Inches till Overflow, \
                 Outfall status, Collection Status','Hours of Operation')
    fopen.write('\n')

  fopen.write("{},{},{},{},{},{},{}".format(start_time, end_time, amount_rain 
                                         ,pool_level, outfall, status, operation))
  fopen.write("\n")
  fopen.close()

################ Rainfall Thread Functions ############

def receive_voltage(voltage_queue):
  '''
  Paramter: voltage_queue( list for voltages)
  Function: Checks the list if voltage has been recieved. If voltage is received,
  Updates voltage file with received voltage
  Returns: None
  '''
  message = ""
  if len(voltage_queue) != 0:
    message = voltage_queue.pop(0)
    if len(message) > 1:
      if message[0] == 'v':
        voltage_val = remove_character(message,'v')
        set_value_file(VOLTAGE,voltage_val)

def send_confirmation(trigger_queue,sender_queue,voltage_queue):
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
    check_end_day()
    receive_voltage(voltage_queue)
    while len(trigger_queue) != 0:
      message = trigger_queue.pop(0)
      if message == "tri":
        sender_queue.append("tyes")
        flag = True
        break

def receive_data(rain_queue,sender_queue,voltage_queue):
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
  receive_voltage(voltage_queue)

  sender_queue.append("ryes")
  set_value_file(RAIN,rain_val)
  set_value_file(POOL_LEVEL,pool_val)
  return (rain_val, pool_val)

################ Outfall thread Functions ##############

def check_low_voltage(voltage_level):
  '''
  Paramter: voltage level(string)
  Function: Checks if voltage level is below a certain threshold
  Returns: True if voltage is below the threshold otherwise False
  '''
  if float(voltage_level) <= 6.0:
    return True
  else:
    return False

def send_outfall_conf(out_queue,sender_queue,lcd,led_matrix):
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
      led_matrix.change_color(led_matrix.get_greenImage())

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

def invoke_system(led_matrix,lcd, collection_time):
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
  '''
  Paramter: led matrix(object), start_time(string)
  Function: stops the buzzers and changes led_matrix to green and Logs data 
  Returns: None
  '''
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
  '''
  Paramter: led matrix(object), start_time(string)
  Function: stops the buzzers and changes led_matrix to red and Logs data 
  Returns: None
  '''
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
  sleep(5)
  led_matrix.change_color(led_matrix.get_greenImage())

  
def restart_state(lcd,led_matrix,current_time):
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
  set_value_file(COLLECTION_TIME,current_time)
  set_value_file(RESTART, '1')
  os.system("sudo reboot")

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
    return '1'
  elif len(miss_files) > 0:
    return '0'
  else:
    return '-1'

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

def rain_detection(trigger_queue,rain_queue,voltage_queue,sender_queue,event):
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
  while not event.is_set():
    send_confirmation(trigger_queue,sender_queue,voltage_queue)
    start_timeDate = datetime.datetime.now()
    rain_fall, pool_level = receive_data(rain_queue,sender_queue,voltage_queue)
    end_timeDate = datetime.datetime.now()  
    end_time = '%s:%s:%s'%(end_timeDate.hour,end_timeDate.minute,end_timeDate.second)
    start_time = '%s:%s:%s'%(start_timeDate.hour,start_timeDate.minute,start_timeDate.second)
    if check_operation_hours(start_timeDate) and check_operation_days(start_timeDate):
      operation = "Yes"
    else:
      operation = "No"
    logger(start_time, end_time, rain_fall, pool_level, None ,"  -  ","  -  ",operation)

def outfall_detection(lcd,led_matrix,out_queue,sender_queue,event):
  '''
  Paramter: lcd (object), led_matrix(object), out_queue( list for 
  flow sensor triqqers), sender_queue (list for sending information), 
  event (Thread flag)
  Function: Check if there is outfall occuring and consider if the user 
  has collected or missed the sample.
  Returns: None
  '''
  set_value_file(STATUS,'-1')
  while not event.is_set():
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

def transmission(xbee, event):
  '''
  Paramter: xbee(object) event( Thread flag)
  Function: sends messages in the send_queue and receieves messages and
  places in there respect queue
  Returns: None
  '''
  while not event.is_set():
      xbee.receive_message()
      xbee.send_message()

