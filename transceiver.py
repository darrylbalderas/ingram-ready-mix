import serial
import glob
import sys
from time import sleep

'''
This Transmitter class was created for the sole purpose 
of testing our Xbee modules. In our senior design project,
the role of transmitter will be assigned to Team Charlie
since we have to wait for their signal to invoke our functionality
'''

class Transceiver:
  def __init__(self, baud_rate,port_path,xbee_addr):
    self.addr = xbee_addr
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, 
                            baud_rate, timeout=1, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)

  def close_serial(self):
    '''
    Stops Xbee connection 
    '''
    self.ser.close()
    
  def reset_serial(self):
    '''
    Reset Serial connection and creates a new Serial Connection
    '''    
    self.ser.close()
    self.ser = serial.Serial(self.port_path, 
                            baud_rate, timeout=1, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    
  def send_message(self,message):
    if self.ser.isOpen():
    # if not '\n' in message:
    #   message = message + '\n'
      self.ser.write(message)

  # def receive_message(self):     
  # # sent message must have a newline character
  #   message = self.ser.readline()
  #   return message 
  def receive_message(self):
    if self.ser.isOpen():
<<<<<<< HEAD
      message = self.ser.read(self.ser.inWaiting())
      return message
    else:
      message = ""
||||||| merged common ancestors
      message = self.ser.read(ser.inWaiting())
=======
      message = self.ser.read()
      self.ser.flush()
      return message
    else:
      return ""
>>>>>>> e7817aee0d07cbcce6129c279964178a68dd9610


















