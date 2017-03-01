import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep


def xbee_usb_port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
    
  for port in ports:
      try:
          ser = serial.Serial(port)
          ser.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass
  return result[0]

def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  tri_conf = ""
  pl_conf = ""
  terminate = ""
  print('about to enter the while loop')
  while not tri_conf == 'ctri\n':
    print('hello')
    for x in range(5):
      xbee.send_message('tri\n')

    for x in range(5):
      tri_conf = xbee.receive_message()

  while not pl_conf == 'cpl\n':

    for x in range(5):
      xbee.send_message('1.43')

    for x in range(5):
      pl_conf = xbee.receive_message()

  while not terminate == "term\n":
    for x in range(5):
      xbee.send_message('fterm\n')

    for x in range(5):
      terminate = xbee.receive_message()

  while not trash == "fin\n":
    for x in range(5):
      xbee.send_message('fin\n')
  break

    

  print('Done')

if __name__ == "__main__":
  main()

