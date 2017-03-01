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
  print('about to enter the while loop')
  while True:
    print('hello')
    for x in range(5):
      xbee.send_message('tri\n')

    for x in range(5):
      tri_conf = xbee.receive_message()

    if tri_conf ==  "ctri\n":
      print('breaking from first while loop')
      break 

if __name__ == "__main__":
  main()

