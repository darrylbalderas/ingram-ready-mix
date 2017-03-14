import sys
import os 
import sys
import os
from time import sleep
import glob
import serial
from time import time
import RPi.GPIO as GPIO
from transceiver import Transceiver
from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor

rain_guage_pin = 18
level_sensor_pin = 23
flow_meter_pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_meter_pin,GPIO.IN)
GPIO.setup(level_sensor_pin,GPIO.IN)
GPIO.setup(rain_guage_pin,GPIO.IN)

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

def detect_outfall(xbee,flow_sensor,level_sensor):
	while True: 
		while flow_sensor.check_outfall() and level_sensor.check_overflow():
	  		#block
	  		xbee.send_message('out\n')
	  		sleep(0.5)
	  		if xbee.receive_message() == 'yes':
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
	pool_val = level_sensor.get_pool_level()
	#block
	message = ""
	create_trigger(xbee)
	while not message == "yes":
		xbee.send_message(rain_val)
		sleep(0.5)
		xbee.send_message(pool_val)
		sleep(0.5)
		message  = xbee.receive_message()
	#endblock
