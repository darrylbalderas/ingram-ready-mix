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

class Transmitter:
  def __init__(self, baud_rate,port_path,xbee_addr):
    self.addr = xbee_addr
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, baud_rate, timeout=1, writeTimeout = 1)
    sleep(1)  #this is to ensure that serial communication is initialize 

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
    self.ser = serial(self.port_path,self.baud_rate, timeout=1)

  def send_message(self,message):
    self.ser.write(message)
    sleep(1)

  def check_message(code,message):

    return code == message

  def receive_message(self):

    message = self.ser.readline()
     # sent message must have a newline character
    self.ser.flush()
    return message 
















