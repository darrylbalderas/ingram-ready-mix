import serial
import glob
import sys
from time import sleep 
from xbee import ZigBee
# from time import sleep

class Transmitter:
  def __init__(self, baud_rate,port_num,SHSL):
    self.SHSL = SHSL
    self.port_number = port_num
    self.baud_rate = baud_rate
    self.connection = serial.Serial(self.port_number, self.baud_rate)
    self.xb = ZigBee(self.connection)

  def stopZigBee(self):
    self.xb.halt()
    self.connection.close()
    
  def resetZigBee(self):
    self.connection.close()
    self.connection = serial(self.port_number,self.baud_rate)

  def send_data(self,frame_id,dest_addr_long,dest_addr,data):
    self.xb.send('tx',frame_id=frame_id,
                 dest_addr_long = dest_addr_long,
                 dest_addr=dest_addr,
                 data = data)

  def receive_data(self):
    message = self.xb.wait_read_frame()
    print(message)

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

  charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E'

  broadcaster = b'\xFF\xFE'
  coordinator = b'\x00\x00'

  usb_list = xbee_Usb_Port()
  xbee = Transmitter(9600,usb_list[0],bravo_SHSL)
  xbee.send_data(frame_id = b'\x01', 
            dest_addr_long = charlie_SHSL,
            dest_addr = broadcaster, data= b'\x11')
  xbee.receive_data()
  xbee.stopZigBee()


if __name__ == '__main__':
  main()


