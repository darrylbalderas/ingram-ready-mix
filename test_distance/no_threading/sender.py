import sys
import glob
import serial
from transceiver import Transceiver
from time import sleep

def xbee_usb_port():
  '''
  Paramter: None
  Function: Looks for the port used by the XBee 
  Returns: port used by XBee
  '''
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial-DN01IUO8')
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

def detect_outfall(xbee):
  message = ""
  xbee.send_message('hey')
  if xbee.receive_message() == 'hey':
    message = xbee.receive_message()
    if message == 'hey':
      print("got it ")


port = xbee_usb_port()
xbee = Transceiver(9600,port)
while True:
   message = raw_input('Enter the trigger:')
   if message == 'y':
    detect_outfall(xbee)

