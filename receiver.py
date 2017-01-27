import serial
import glob
import sys
from time import sleep 

#from xbee import XBee 

'''
This Receiver class will resemble our bravo xbee module.
'''

class Receiver:
  def __init__(self, baud_rate,port_path,xbee_SHSL, xbee_MY):
    self.SHSL = xbee_SHSL
    self.MY = xbee_MY
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, baud_rate, timeout=1)
    sleep(2) # this is to ensure that serial communication is initialize 

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
        print('received')
        self.write('yes')
        flag = True
      else:
        print('not received')
        self.write('no')
        message.self.readline()
        print(message)

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

# def toHex(sample):
#   '''
#   Changes a bit string and converts it to Hexadecimal 
#   '''
#   lst = []
#   for ch in sample:
#       hv = hex(ord(ch)).replace('0x', '')
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

def main():
  usb_list = xbee_Usb_Port()
  default_coordinator = b'\x00\x00\x00\x00\x00\x00\x00\x00'
  charlie_SHSL = b'\x00\x13\xA2\x00\x41\x04\x96\x6E'
  charlie_MY = b'\x00\x00'

  charlie_xbee = Receiver(9600,usb_list[0],charlie_SHSL,charlie_MY)

    


    

if __name__ == '__main__':
  main()


