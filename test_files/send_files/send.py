import sys 
import glob
import serial 
from transceiver import Transceiver
from threading import Thread
import datetime
from time import sleep

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
      elif send_flag == True:
        sender_queue.append("tri")
        send_flag = False

def send_data(rain_queue,send_queue):
  tmp_pool_val = 12.0
  tmp_rain_val = 2.12
  pool_val = 'p' + str(tmp_pool_val)
  rain_val = 'r' + str(tmp_rain_val)
  message = ""
  flag = False
  send_flag = True
  while not flag:
    time_date = datetime.datetime.now()
    if len(rain_queue) != 0:
        message = rain_queue.pop(0)
        if message == "ryes":
          print('got confirmation')
          flag = True
        else:
            send_flag = True
    elif send_flag == True:
        send_queue.append(rain_val)
        send_queue.append(pool_val)
        send_flag = False

def send_outfall(out_queue, sender_queue):
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
    elif send_flag == True:
        sender_queue.append("out")
        send_flag = False

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

  if port != None:
    charlie_xbee = Transceiver(9600,port,out_queue,trigger_queue,rain_queue,sender_queue)
    thread1 = Thread(target = transmission, args = (charlie_xbee,))
    thread1.start()
    sleep(0.5)
    while True:
      user_input = raw_input("Enter an input \
                              \n (V) for voltage \
                              \n (R) for voltage \
                              \n (O) for outfall \
                              \n (N) for ending program\n")
      if user_input.lower() == 'v':
        user_input = raw_input("Enter Voltage: ")
        str_voltage = 'v'+str(user_input)
        sender_queue.append(str_voltage)
      elif user_input.lower() == 'r':
        create_trigger(trigger_queue, sender_queue)
        send_data(rain_queue,sender_queue)
      elif user_input.lower() == 'o':
        send_outfall(out_queue,sender_queue)
  else:
    print("No Xbee connected")


if __name__ == "__main__":
  main()
