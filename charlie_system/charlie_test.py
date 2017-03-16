import sys
import os 
import sys
import os
from time import sleep
import glob
import serial
from time import time
import RPi.GPIO as GPIO

rain_guage_pin = 18
level_sensor_pin = 23
flow_sensor_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor_pin,GPIO.IN)
GPIO.setup(level_sensor_pin,GPIO.IN)
GPIO.setup(rain_guage_pin,GPIO.IN)

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
        print("checking for outfall")
        while True:
		while flow_sensor.check_outfall() and level_sensor.check_value():
	  		#block
                        print("outfall is occuring")
	  		xbee.send_message('out\n')
	  		sleep(0.2)
	  		if xbee.receive_message() == 'yes':
                                print("got confirmation")
	  			break
	  		#endblock

def detect_rainfall(rain_guage,xbee,level_sensor):
	while True:
		if rain_guage.get_tick():
			#block
			create_trigger(xbee)
			#endblock
			send_data(xbee,rain_guage,level_sensor)

def create_trigger(xbee):
	status = False
	while not status:
		xbee.send_message('tri\n')
		message = xbee.receive_message()
		if message == "yes":
			status = True

def send_data(xbee,rain_gauge,level_sensor):
	pool_val = level_sensor.get_pool_level()
	rain_val = rain_gauge.get_total_rainfall()
	print('got rainfall ')
	pool_val = level_sensor.get_pool_level()
	print('got pool level')
	pool_val = 'p' + str(pool_val) + '\n'
	rain_val = 'r' + str(rain_val) + '\n'
	#block
	message = ""
	create_trigger(xbee)
	print('Got trigger')
	while not message == "yes":
		xbee.send_message(rain_val)
		sleep(0.5)
		xbee.send_message(pool_val)
		sleep(0.5)
		message  = xbee.receive_message()
	print('finish sending the data')
	#endblock
