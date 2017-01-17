import serial
import glob
import sys
from xbee import XBee 
# from xbee.base import XBeeBase
# from xbee.frame import APIFrame
# from xbee import ZigBee
# from time import sleep

class Transmitter:
  def __init__(self, baud_rate, port_path, SHSL):
    self.SHSL = SHSL
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, self.baud_rate)
    self.xbee = XBee(self.ser, escaped=True)

  def stopXBee(self):
    self.xbee.halt()
    self.ser.close()
    
  def resetXBee(self):
    self.ser.halt()
    self.ser.close()
    self.ser = serial(self.port_number,self.baud_rate)

  def send_data(self,dest_addr_long,data):
    self.xbee.tx_long_addr(dest_addr_long=dest_addr_long, data=data)

  def receive_data(self):
    message = self.xbee.wait_read_frame()
    return message

  def get_SHSL(self):
    return self.SHSL

  def set_SHSL(self,SHSL):
    self.SHSL = SHSL


def toHex(sample):
    lst = []
    for character in sample:
        hv = hex(ord(character)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        hv = '0x' + hv
        lst.append(hv)

def decodeReceivedFrame(data):
            source_addr_long = toHex(data['source_addr_long'])
            source_addr = toHex(data['source_addr'])
            xBee_id = toHex(data['id'])
            samples = toHex(data['samples'])
            return [source_addr_long, source_addr, xBee_id, samples]


def xbee_Usb_Port():
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usb*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/tty[A-Za-z]*')
  for port in ports:
      try:
          ser = serial.Serial(port)
          ser.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass

  return result


def main():
  bravo_SHSL = b'\x00\x13\xA2\x00\x41\x03\xF0\xFF'
  #charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E'
  default_broadcaster = b'\x00\x00\x00\x00\x00\x00\xFF\xFF'
  sending_data = b'\x11'

  usb_list = xbee_Usb_Port()

  bravo_xbee = Transmitter(9600,usb_list[0],bravo_SHSL)

  flag = False

  while not flag:
    try:
      bravo_xbee.send_data(dest_addr_long = default_broadcaster, data=sending_data)
      #sleep(0.1)
      data = bravo_xbee.receive_data()    

      if data['deliver_status'] != b'"':
        print("Data has been received ")
        flag = True
      else:
        print("Data has not been received")

    except KeyboardInterrupt:
      break

  bravo_xbee.stopXBee()


if __name__ == '__main__':
  main()


