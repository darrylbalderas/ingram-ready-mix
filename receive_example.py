import serial
from transceiver import Transceiver
import glob
import sys

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
  trigger = ""
  pool_level = ""
  while not trigger == 'tri\n':
    print('in loop')
    for x in range(5):
      trigger = xbee.receive_message()

    if trigger == "tri\n":
      for x in range(5):
        xbee.send_message('ctri\n')

  while pool_level != "" 
    for x in range(5):
      pool_level = xbee.receive_message()


  while not fterminate == "fterm\n"
      for x in range(5):
        xbee.send_message('cpl\n')

      for x in range(5):
        fterminate = xbee.receive_message()

  while not trash == "fin\n":
    for x in range(5):
      xbee.send_message('term\n')

    for x in range(5):
      trash = xbee.receive_message()
  break

  while not 


  break



    

if __name__ == "__main__":
  main()

