import sys
import glob
import serial
from transceiver import Transceiver
from threading import Thread

def xbee_usb_port():
  '''
  Paramter: None
  Function: Looks for the port used by the XBee 
  Returns: port used by XBee
  '''
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial-DN01IVXV')
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

# # def transmission(xbee):
# #   while True:
# #     xbee.send_message()
# #     xbee.receive_message()

def sender(xbee):
  while True:
    xbee.send_message()

def receiver(xbee):
  while True:
    xbee.receive_message()


def send_confirmation(receive_queue,sender_queue):
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
    while len(receive_queue) != 0:
      message = receive_queue.pop(0)
      if message == "hey":
        sender_queue.append("hey")
        flag = True
        break

def main():
  port =  xbee_usb_port()
  sender_queue = [ ]
  receiver_queue = [ ]
  message_count = 0
  if port != None:
    xbee = Transceiver(9600,port,receiver_queue,sender_queue)
    thread1 = Thread(target=receiver, args=(xbee,))
    thread1.start()
    thread2 = Thread(target=sender, args=(xbee,))
    thread2.start()
    while True:
        send_confirmation(receiver_queue,sender_queue)
        message_count += 1
        print("got it")
  else:
    port('Missing Xbee module')

if __name__ == "__main__":
  main()
