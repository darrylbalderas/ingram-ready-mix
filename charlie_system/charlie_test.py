import sys
import os 
from time import sleep
import glob
import serial
from time import time
import RPi.GPIO as GPIO
import datetime
from datetime import monthrange

OUTFALL = './config_files/outfall_val.txt'

rain_guage_pin = 18
level_sensor_pin = 23
flow_sensor_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor_pin,GPIO.IN)
GPIO.setup(level_sensor_pin,GPIO.IN)
GPIO.setup(rain_guage_pin,GPIO.IN)

def initialize_files():
  files = {'outfall': OUTFALL
          }
  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')

  for key,value in files.items():
    if os.path.exists(value):
      fopen = open(value, 'w')
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

def calculate_days():
  time_date = datetime.datetime.now()
  month, days_left = monthrange(time_date.year,time_date.month)
  time_left = (days_left - time_date.day) * 24 * 60 * 60
  return time_left

def calculate_hours():
  time_date = datetime.datetime.now()
  hour_left = (24 - time_date.hour) * 60 * 60
  return hour_left

def xbee_usb_port():
	if sys.platform.startswith('linux'):
	    ports = glob.glob('/dev/ttyUSB0')
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

def detect_outfall(xbee, flow_sensor,level_sensor):
	while True:
		while flow_sensor.check_outfall() and level_sensor.check_value():
	  		xbee.send_message('out\n')
	  		sleep(0.5)
	  		if xbee.receive_message() == 'oyes':
	  			break
	  		sleep(calculate_hours)
	  	
def detect_rainfall(rain_guage,xbee,level_sensor):
	while True:
		if rain_guage.get_tick():
			create_trigger(xbee)
			send_data(xbee,rain_guage,level_sensor)

def create_trigger(xbee):
	message = ""
	while not message == "tyes":
		xbee.send_message('tri\n')
		message = xbee.receive_message()

def send_data(xbee,rain_gauge,level_sensor):
	pool_val = level_sensor.get_pool_level()
	rain_val = rain_gauge.get_total_rainfall()
	pool_val = level_sensor.get_pool_level()
	pool_val = 'p' + str(pool_val) + '\n'
	rain_val = 'r' + str(rain_val) + '\n'
	message = ""
	create_trigger(xbee)
	while not message == "ryes":
		xbee.send_message(rain_val)
		sleep(0.5)
		xbee.send_message(pool_val)
		sleep(0.5)
		message  = xbee.receive_message()
