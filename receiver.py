import serial
import glob
import sys
from time import sleep 
from xbee import ZigBee
# from time import sleep

class Transmitter:
  def __init__(self, baud_rate,port_num):
    self.port_number = port_num
    self.baud_rate = baud_rate
    self.connection = serial.Serial(self.port_number, baud_rate)
    self.xb = ZigBee(self.connection)


  def stopUsbConnection(self):
    self.connection.close()
    
  def resetUsbConnection(self):
    self.connection.close()
    self.connection = serial(self.port_number,self.baud_rate)


def xbee_Usb_Port():
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usb*')
  else:
    ports = glob.glob('/dev/tty[A-Za-z]*')
  result = []
  for port in ports:
      try:
          s = serial.Serial(port)
          s.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass
  return result

def main():
  usb_list = xbee_Usb_Port()
  # Create API object
  xbee = Transmitter(9600,usb_list[1])


if __name__ == '__main__':
  main()


