import sys 
import glob
import serial 
from transceiver import Transceiver
from threading import Thread
from threading import Event 
import random
from time import sleep 
import datetime

def xbee_usb_port():
  if sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
  elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
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

def transmission(xbee):
  switch_flag = False
  while True:
    if switch_flag ==  False:
      xbee.receive_message()
      switch_flag = True
    else:
      xbee.send_message()
      switch_flag = False

def main():
  sender_queue= [ ]
  out_queue = [ ]
  trigger_queue = [ ]
  rain_queue = [ ]
  port = xbee_usb_port()
  event = Event()
  if port != None:
    charlie_xbee = Transceiver(9600,port,out_queue,trigger_queue,rain_queue,sender_queue)
    thread1 = Thread(target = transmission, args = (charlie_xbee,event,))
    thread1.start()
    sleep(0.5)
    voltages = ['12.3','11.7','11.8','11.9','12.9','13.6']
    while True:
      time_date = datetime.datetime.now()
      if time_date.second%5 == 0:
        voltage = random.choice(voltages)
        str_voltage = 'v'+str(voltage)
        sender_queue.append(str_voltage)
  else:
    print("No Xbee connected")

if __name__ == "__main__":
  main()
