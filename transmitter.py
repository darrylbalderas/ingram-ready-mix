import serial
import glob
import sys
from xbee import XBee 
# from xbee.base import XBeeBase
# from xbee.frame import APIFrame
# from xbee import ZigBee
# from time import sleep

'''
This Transmitter class was created for the sole purpose 
of testing our Xbee modules. In our senior design project,
the role of transmitter will be assigned to Team Charlie
since we have to wait for their signal to invoke our functionality
'''

class Transmitter:
  def __init__(self, baud_rate,port_path,xbee_SHSL, xbee_MY):
    self.SHSL = xbee_SHSL
    self.MY = xbee_MY
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, baud_rate, timeout=1)
    sleep(2)  #this is to ensure that serial communication is initialize 

  def stopXBee(self):
    '''
    Stops Xbee connection 
    '''
    self.ser.close()
    
  def resetXBee(self):
    '''
    Reset Serial connection and creates a new Serial Connection
    '''    
    self.ser.close()
    self.ser = serial(self.port_path,self.baud_rate, timeout=1)
 
  def send_data(self, message):
    '''
    Sends data to another Xbee with a certain destition address specified
    '''
    # message = b'\x7E\x00\x13\x10\x01'+ dest_addr_long + dest_addr + data + b'\n' 
    
    flag = False
    self.write(message)
    confirmation = self.readline()
    while not flag :
      if confirmation.decode('ascii') != 'yes': 
        self.write(message)
        confirmation = self.readline()
      else:
        print('sent')
        flag = True



  def receive_data(self, data):
    '''
    Waits until a message is received 
    '''
    # return message
    message = self.readline()
    flag = False
    while not flag:
      if message.decode('ascii') == data:
        self.write('yes')
        print('received')
        flag = True
      else:
        self.write('no')
        print('not received')
        message.self.readline()
    return message 


  def get_SHSL(self):
    '''
    Returns 64bit Xbee address
    '''
    return self.SHSL

  def set_SHSL(self,SHSL):
    '''
    Changes the 64bit Xbee address
    '''
    self.SHSL = SHSL
  def get_MY(self):
    '''
    Returns 16bit Xbee address
    '''
    return self.MY

  def set_MY(self,MY):
    '''
    Changes the 64bit Xbee address
    '''
    self.MY = MY

# def toHex(sample):
#   '''
#   Changes a bit string and converts it to Hexadecimal 
#   '''
#   lst = []
#   for character in sample:
#       hv = hex(ord(character)).replace('0x', '')
#       if len(hv) == 1:
#           hv = '0'+hv
#       hv = '0x' + hv
#       lst.append(hv)

# def decodeReceivedFrame(data):
#   '''
#   Data received from the Xbee is received in a dictionary.
#   This function decodes using keys and returns a list with values 
#   associated with those keys
#   '''
#   source_addr_long = toHex(data['source_addr_long'])
#   source_addr = toHex(data['source_addr'])
#   xBee_id = toHex(data['id'])
#   samples = toHex(data['samples'])
#   return [source_addr_long, source_addr, xBee_id, samples]


def xbee_Usb_Port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
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
  usb_list = xbee_Usb_Port()
  bravo_SHSL = b'\x00\x13\xA2\x00\x41\x03\xF0\xFF'
  bravo_MY = b'\xFF\xFE'
  charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E' 

  bravo_xbee = Transmitter(9600,usb_list[0],bravo_SHSL,bravo_MY)

  


  # flag = False

  # while not flag:
  #   try:
  #     bravo_xbee.send_data(dest_addr_long=default_broadcaster, data=sending_data)
  #     data = bravo_xbee.receive_data()    

  #     if data['deliver_status'] != b'"':

  #       print("Data has been received ")
  #       flag = True
  #     else:
  #       print("Data has not been received")

  #   except KeyboardInterrupt:
  #     break

  # bravo_xbee.stopXBee()


if __name__ == '__main__':
  main()


