import sys
import os 
from time import sleep
import glob
import serial
import RPi.GPIO as gpio
import datetime
from time import time 

global RESTART_HOLD 
RESTART_HOLD = 3 

OUTFALL_DATE = './config_files/outfall_date.txt'
RAIN = './config_files/rain_val.txt'
POOL_LEVEL = './config_files/pool_level.txt'
RESTART = './config_files/restart.txt'


pin_dictionary = { 'rain': 12,
                   'flow': 10,
                   'restart': 8
                 }

gpio.setmode(gpio.BOARD)
gpio.setup(pin_dictionary['flow'], gpio.IN)
gpio.setup(pin_dictionary['rain'], gpio.IN)
gpio.setup(pin_dictionary['restart'], gpio.IN)

######## Helper Functions ########

def initialize_files():
  files = {'rain': RAIN
           ,'date': OUTFALL_DATE
           ,'pool': POOL_LEVEL
           ,'restart': RESTART
          }

  if not os.path.exists('./config_files'):
    os.system('mkdir config_files')

  for key,value in files.items():
    if os.path.exists(value):
      fopen = open(value, 'w')
      if key == 'date':
      	fopen.write('None')
      elif key == 'rain':
      	fopen.write('0.1690')
      elif key == 'pool':
      	fopen.write('12')
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

def check_restart():
	return gpio.input(pin_dictionary['restart'])

def restart_state():
  state  = 0
  end_time = 0
  start_time = time()
  while end_time < RESTART_HOLD:
    end_time = time() - start_time
    state = check_restart()
    if not state:
      return
  os.system("sudo reboot")

def calculate_sleep():
	time_date = datetime.datetime.now()
	time_sleep = (24 - time_date.hour) * 60 * 60
	return time_sleep



######## Charlie Main Program Functions ########

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

def check_voltage_interval(send_queue,battery):
	time_date = datetime.datetime.now()
	if time_date.minute == 59:
		if time_date.second >= 0 and time_date.second <= 5:
			voltage = battery.get_voltage_level()
			send_queue.append(str(voltage))
	
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

def send_data(rain_gauge,level_sensor,rain_queue,send_queue,battery):
	tmp_pool_val = level_sensor.get_pool_level()
	tmp_rain_val = rain_gauge.get_total_rainfall(pin_dictionary['restart'],RESTART_HOLD)
	tmp_pool_val = level_sensor.get_pool_level()
	pool_val = 'p' + str(tmp_pool_val)
	rain_val = 'r' + str(tmp_rain_val)
	message = ""
	flag = False
	send_flag = True
	while not flag:
	    if len(rain_queue) != 0:
	        message = rain_queue.pop(0)
	        if message == "ryes":
	            flag = True
	        else:
	            send_flag = True
	    elif send_flag:
	        send_queue.append(rain_val)
	        send_queue.append(pool_val)
	        send_flag = False
	    check_voltage_interval(send_queue,battery)

######## Thread Functions ########

def detect_rainfall(rain_guage,level_sensor,tri_queue,rain_queue,send_queue,battery,event):
	while not event.is_set():
		check_voltage_interval(send_queue,battery)
		if check_restart():
			restart_state()
		if rain_guage.get_tick():
			create_trigger(tri_queue,send_queue)
			send_data(rain_guage,level_sensor,rain_queue,send_queue,battery)

def detect_outfall(flow_sensor,level_sensor,out_queue,send_queue,event):
	while not event.is_set():
		if flow_sensor.check_outfall() and level_sensor.check_overflow():
			time_date = datetime.datetime.now()
			outfall_date = "%s/%s"%(time_date.month,time_date.day,time_date.year)
			if check_value_file(OUTFALL_DATE) == outfall_date:
				time_sleep = calculate_sleep()
				sleep(time_sleep)
			else:
				send_outfall(out_queue,send_queue)
				set_value_file(OUTFALL_DATE,outfall_date)

def transmission(xbee,event):
    while not event.is_set():
        xbee.receive_message()
        xbee.send_message()
