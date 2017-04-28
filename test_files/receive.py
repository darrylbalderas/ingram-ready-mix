import sys 
import glob
import serial 
from transceiver import Transceiver
from threading import Thread
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

def remove_character(message,character):
  '''
  Parameters: string, string
  Function: Remove desired character from the message
  Returns: Message without the character in the parameters
  '''
  return message.strip(character)

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
    if len(message)  >= 3:
      if message[0] == 'v':
        voltage_val = remove_character(message,'v')
        print(voltage_val)

def send_outfall_conf(out_queue,sender_queue):
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
  while not flag:
    while len(out_queue) != 0:
      message = out_queue.pop(0)
      if message == "out":
        sender_queue.append("oyes")
        flag = True
        break

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
    receive_voltage(voltage_queue)
    while len(trigger_queue) != 0:
      message = trigger_queue.pop(0)
      if message == "tri":
        print(message)
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
      print(message)
      if message[0] == 'r' and not rain_flag:
        rain_val = remove_character(message,'r')
        rain_flag = True
      elif message[0] == 'p'and not pool_flag:
        pool_val = remove_character(message,'p')
        pool_flag = True
  sender_queue.append("ryes")
  return (rain_val, pool_val)

def outfall(out_queue,sender_queue):
  while True:
    send_outfall_conf(out_queue,sender_queue) 
    print('got outfall it')

def rain(trigger_queue,rain_queue,voltage_queue,sender_queue):
  while True:
    send_confirmation(trigger_queue,sender_queue,voltage_queue)
    print('got conf')
    rain_fall, pool_level = receive_data(rain_queue,sender_queue,voltage_queue)
    print('got data')

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
  voltage_queue = [ ]
  port = xbee_usb_port()
  if port != None:
    xbee = Transceiver(9600,port,out_queue,trigger_queue,rain_queue,voltage_queue,sender_queue)
    thread1 = Thread(target = outfall, args = (out_queue,sender_queue,))
    thread1.start()
    sleep(1)
    thread2 = Thread(target = rain, args = (trigger_queue,rain_queue,voltage_queue,sender_queue,))
    thread2.start()
    sleep(1)
    transmission(xbee)
  else:
    print("No Xbee connected")


if __name__ == "__main__":
  main()
