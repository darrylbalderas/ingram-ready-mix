import serial
import glob
import sys
from xbee.base import XBeeBase
from xbee.frame import APIFrame
from xbee import ZigBee
# from time import sleep

class Transmitter:
  def __init__(self, baud_rate, port_path, SHSL):
    self.SHSL = SHSL
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, self.baud_rate)
    self.xbee = ZigBee(self.ser)

  def stopZigBee(self):
    self.xbee.halt()
    self.ser.close()
    
  def resetZigBee(self):
    self.ser.close()
    self.ser = serial(self.port_number,self.baud_rate)

  def send_data(dest_addr_long, dest_addr, data):
    self.xbee.send('tx',dest_addr_long = dest_addr_long, dest_addr=dest_addr, data=data)

  def receive_data(self):
    message = self.xbee.wait_read_frame()
    return message

  def get_SHSL(self):
    return self.SHSL

  def set_SHSL(self,SHSL):
    self.SHSL = SHSL


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
  bravo_SHSL = b'\x00\x13\xA2\x00\x41\x03\xF0\xFF'
  default_coordinator = b'\x00\x00\x00\x00\x00\x00\x00\x00'

  charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E'
  default_broadcaster = b'\x00\x00\x00\x00\x00\x00\xFF\xFF'

  broadcaster = b'\xff\xff'
  sending_data = b'\x11'
  # coordinator = b'\x00\x00'


  usb_list = xbee_Usb_Port()

  xbee = Transmitter(9600,usb_list[0],bravo_SHSL)
  flag = False
  while not flag:
    try:
      xbee.xbee.send('tx',dest_addr_long = default_broadcaster, dest_addr=broadcaster, data=sending_data)
      data = xbee.receive_data()    
      # print(data)
      if data['deliver_status'] != b'"':
        flag = True
        print("Data has been received ")
      else:
        print("Data has not been received")

    except KeyboardInterrupt:
      break

  xbee.stopZigBee()


if __name__ == '__main__':
  main()


