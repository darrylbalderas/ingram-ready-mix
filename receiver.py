import serial
import glob
import sys
from time import sleep 
from xbee import ZigBee

# from time import sleep

class Receiver:
  def __init__(self, baud_rate,port_path,SHSL):
    self.SHSL = SHSL
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, baud_rate, timeout = 1)
    self.xbee = ZigBee(self.ser)

  def stopZigBee(self):
    self.xbee.halt()
    self.ser.close()
    
  def resetZigBee(self):
    self.ser.close()
    self.ser = serial(self.port_path,self.baud_rate)
 
  def send_data(self,frame_id,dest_addr_long,dest_addr,data):
    self.xbee.send('tx',frame_id=frame_id,
                 dest_addr_long = dest_addr_long,
                 dest_addr=dest_addr,
                 data = data)

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

  charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E'
  default_coordinator = b'\x00\x00\x00\x00\x00\x00\x00\x00'
  bravo_SHSL = b'\x00\x13\xA2\x00\x41\x03\xF0\xFF'
  coordinator = b'\x00\x00'
  sending_data = b'\x11'

  usb_list = xbee_Usb_Port()
  charlie_xbee = Receiver(9600,usb_list[0],charlie_SHSL)
  charlie_xbee.xbee.send('tx',dest_addr_long = default_coordinator,
                         dest_addr = coordinator, data = b'\x11')
  data = charlie_xbee.receive_data()

  flag = False

  while not flag:
    data = charlie_xbee.receive_data()
    if data['id'] == 'tx_status':
      charlie_xbee.xbee.send('tx', dest_addr_long = default_coordinator,dest_addr = coordinator, data =sending_data)
      data = charlie_xbee.receive_data()
      print(data['deliver_status'])
    elif data['id'] == 'rx':
      print(data['rf_data'])
      flag = True
  charlie_xbee.stopZigBee()
    

if __name__ == '__main__':
  main()


