import sys
import os 
from time import sleep
import glob
import serial
import RPi.GPIO as gpio
import datetime

global EXIT_FLAG 
EXIT_FLAG = False

############### Global Variables #################

OUTFALL_DATE = './config_files/outfall_date.txt'
PREV_VOLTAGE = './config_files/pre_voltage.txt'

pin_dictionary = { 'rain': 12,
                   'flow': 10,
                 }

start_shift = 6
end_shift = 17  # change back to 17
first_work_day = 0
last_work_day = 5 # change back to 5

############### GPIO Functions #################
gpio.setmode(gpio.BOARD)
gpio.setup(pin_dictionary['flow'], gpio.IN)
gpio.setup(pin_dictionary['rain'], gpio.IN)

############### Helper Functions #################

def initialize_files():
  files = {
           'date': OUTFALL_DATE,
           'voltage': PREV_VOLTAGE
          }

  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')

  for key,value in files.items():
    if not os.path.exists(value):
      fopen = open(value, 'w')
      if key == 'date':
      	fopen.write('None')
      elif key == 'voltage':
      	fopen.write('12.0')
      else:	
      	fopen.write('0')
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

def get_pins():
	return pin_dictionary

def xbee_usb_port():
	if sys.platform.startswith('linux'):
	    ports = glob.glob('/dev/ttyU*')
	if len(ports) != 0:
		result = []
		for port in ports:
			try:
				ser = serial.Serial(port)
				ser.close()
				result.append(port)
			except( OSError, serial.SerialException):
				pass
		return result[0]
	else:
		return None

def calculate_sleep():
  time_date = datetime.datetime.now()
  time_sleep = ((24 - time_date.hour) * 60 * 60) - (time_date.minute*60) - (time_date.second)
  return time_sleep

def check_operation_hours(time_date):
  current_hour = time_date.hour
  current_min = time_date.minute
  working_hours = False
  if current_hour >= start_shift and current_hour < end_shift:
    if current_hour ==(end_shift-1) and current_min > 58:
      working_hours = False
    else:
      working_hours = True
  else:
    working_hours = False
  return working_hours

def check_operation_days(time_date):
  working_days = False
  if time_date.weekday() >= first_work_day and time_date.weekday() < last_work_day:
    working_days = True
  else:
    working_days = False
  return working_days

################ Outfall Thread Functions #############

def send_outfall(out_queue, send_queue):
  message = ""
  flag = False
  send_flag = True
  while not flag:
    time_date = datetime.datetime.now()
    if len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "oyes":
        flag = True
      else:
        send_flag = True
    elif send_flag == True or time_date.second%3==0:
      send_queue.append("out")
      send_flag = False

############## Rainfall Thread Functions ###############

def check_voltage(send_queue,battery):
  time_date = datetime.datetime.now()
  if time_date.minute == 30:
    voltage = battery.get_voltage_level()
    set_value_file(PREV_VOLTAGE,str(voltage))
  previous_voltage = check_value_file(PREV_VOLTAGE)
  voltage = battery.get_voltage_level()
  voltage_difference = abs(round(voltage-float(previous_voltage),1))
  if voltage_difference >= 0.1:
    set_value_file(PREV_VOLTAGE,str(voltage))
    send_queue.append('v'+str(voltage))
	
def create_trigger(trigger_queue,sender_queue):
  message = ""
  flag = False
  send_flag = True
  while not flag:
    time_date = datetime.datetime.now()
    if len(trigger_queue) != 0:
      message = trigger_queue.pop(0)
      if message == "tyes":
        flag = True
      else:
        send_flag = True
    elif send_flag == True or time_date.second%3==0:
      sender_queue.append("tri")
      send_flag = False

def send_data(rain_gauge,level_sensor,rain_queue,send_queue,battery):
  tmp_pool_val = level_sensor.get_pool_level()
  tmp_rain_val = rain_gauge.get_total_rainfall()
  tmp_pool_val = level_sensor.get_pool_level()
  pool_val = 'p' + '%.2f'%(tmp_pool_val)
  rain_val = 'r' + '%.3f'%(tmp_rain_val)
  message = ""
  flag = False
  send_flag = True
  while not flag:
    time_date = datetime.datetime.now()
    if len(rain_queue) != 0:
      message = rain_queue.pop(0)
      if message == "ryes":
        flag = True
      else:
        send_flag = True
    elif send_flag == True or time_date.second%3==0:
      send_queue.append(rain_val)
      send_queue.append(pool_val)
      send_flag = False

################# Thread Functions #####################

def detect_rainfall(rain_guage, level_sensor, tri_queue, rain_queue,send_queue,battery):
  while True:
    if rain_guage.get_tick():
      create_trigger(tri_queue,send_queue)
      send_data(rain_guage,level_sensor,rain_queue,send_queue,battery)
    check_voltage(send_queue,battery)

def detect_outfall(flow_sensor,level_sensor,out_queue,send_queue):
  send_flag = False
  previous_value = 0
  while True:
    current_value = flow_sensor.check_flow()
    if current_value > previous_value:
      send_flag = True
      previous_value = current_value
    elif previous_value > current_value:
      send_flag = True
      previous_value = current_value
    else:
      send_flag = False

    if send_flag == True and level_sensor.check_overflow() == 1:
        send_outfall(out_queue,send_queue)
        send_flag = False

def transmission(xbee):
  switch_state_flag = False
  while True:
    if switch_state_flag == False:
      xbee.receive_message()
      switch_state_flag = True
    else:
      xbee.send_message()
      switch_state_flag = False
