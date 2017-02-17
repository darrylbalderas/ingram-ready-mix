import sys
import glob 
import serial
from transceiver import Transceiver

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
  return result

ports = xbee_usb_port()
coor = ports.pop()
xbee1 = Transceiver(9600,coor)
num = 0
while True:
  rain_message = xbee1.receive_message()

  if rain_message == 'rain':
    for i in range(0,10):
      xbee1.send_message('what\n')

      
    

