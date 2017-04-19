import sys
import glob
import serial
from transceiver import Transceiver
from threading import Thread
from time import time

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

# def transmission(xbee):
#   while True:
#     xbee.send_message()
#     xbee.receive_message()

def sender(xbee):
  while True:
    xbee.send_message()

def receiver(xbee):
  while True:
    xbee.receive_message()

def send_hey(receiver_queue, sender_queue):
  message = ""
  flag = False
  send_flag = True
  while not flag:
    if len(receiver_queue) != 0:
      message = receiver_queue.pop(0)
      if message == "hey":
        flag = True
      else:
        send_flag = True
    elif send_flag == True:
        sender_queue.append("hey")
        send_flag = False

def main():
  port =  xbee_usb_port()
  sender_queue = [ ]
  receiver_queue = [ ]
  message_count = 0
  start_time = 0
  end_time = 0
  fopen = open('times.csv','w')
  fopen.write('%s,%s'%('Start_time','End_time'))
  fopen.write('\n')
  if port != None:
    xbee = Transceiver(9600,port,receiver_queue,sender_queue)
    thread1 = Thread(target=receiver, args=(xbee,))
    thread1.start()
    thread2 = Thread(target=sender, args=(xbee,))
    thread2.start()
    while True:
      user_input = raw_input('Enter (Y) to send message: ')
      if user_input.lower() ==  'y':
        message_count += 1
        start_time = time()
        send_hey(receiver_queue,sender_queue)
        end_time = time() - start_time
        print("got confirmation")
        fopen.write('%s,%s'%(0,end_time))
        fopen.write('\n')
      if user_input.lower() == 'n':
        fopen.close()
  else:
    port('Missing Xbee module')

if __name__ == "__main__":
  main()
