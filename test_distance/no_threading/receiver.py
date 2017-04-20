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

def send_outfall_conf(xbee):
  message = ""
  while not message == 'hey':
    message = xbee.receive_message()
  xbee.send_message("hey")

port = xbee_usb_port()
xbee = Transceiver(9600,port)

while True:
  send_outfall_conf(xbee)
  print("got the message")


