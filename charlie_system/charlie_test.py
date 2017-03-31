import sys
import os 
from time import sleep
import glob
import serial
from time import time
import RPi.GPIO as GPIO
import datetime
from calendar import monthrange

OUTFALL = './config_files/outfall_val.txt'

rain_guage_pin = 8
flow_sensor_pin = 10
GPIO.setmode(GPIO.BOARD)
GPIO.setup(flow_sensor_pin,GPIO.IN)
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
  return (days_left - time_date.day)

def calculate_hours():
  time_date = datetime.datetime.now()
  return (24 - time_date.hour)

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

def send_outfall(out_queue, send_queue):
	message = ""
	flag = False
	send_flag = True
	while not flag:
		if len(out_queue) != 0:
			message = out_queue.pop(0)
			if message == "oyes":
				flag = True
			else:
				send_flag = True
		elif send_flag == True:
				send_queue.append("out")
                send_flag = False

def detect_outfall(flow_sensor,level_sensor,out_queue,send_queue):
	while True:
		if flow_sensor.check_outfall() and level_sensor.check_overflow():
			time_date = datetime.datetime.now()
			outfall_date = "%s/%s"%(time_date.month,time_date.year)
			if check_value_file(OUTFALL) == outfall_date:
				while calculate_days() > 0:
					pass
			else:
				send_outfall(out_queue,send_queue)
				set_value_file(OUTFALL,outfall_date)

	  	
def detect_rainfall(rain_guage,level_sensor,tri_queue,send_queue):
	while True:
		if rain_guage.get_tick():
			create_trigger(tri_queue,send_queue)
			send_data(rain_guage,level_sensor,tri_queue,send_queue)

def create_trigger(tri_queue,send_queue):
    message = ""
    flag = False
    send_flag = True
    while not flag:
        if len(tri_queue) != 0:
            message = tri_queue.pop(0)
            if message == "tyes":
                flag = True
            else:
                send_flag = True
        elif send_flag == True:
        	send_queue.append("tri")
        	send_flag = False

def send_data(rain_gauge,level_sensor,tri_queue,send_queue):
	tmp_pool_val = level_sensor.get_pool_level()
	tmp_rain_val = rain_gauge.get_total_rainfall()
	tmp_pool_val = level_sensor.get_pool_level()
	pool_val = 'p' + str(tmp_pool_val)
	rain_val = 'r' + str(tmp_rain_val)
	message = ""
	flag = False
	send_flag = True
	while not flag:
	    if len(tri_queue) != 0:
	        message = tri_queue.pop(0)
	        if message == "ryes":
	            flag = True
	        else:
	            send_flag = True
	    elif send_flag:
	        send_queue.append(rain_val)
	        send_queue.append(pool_val)
	        send_flag = False


def transmission(xbee):
    while True:
        xbee.receive_message()
        xbee.send_message()
