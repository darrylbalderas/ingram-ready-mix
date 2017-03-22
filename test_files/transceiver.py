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
  def __init__(self, baud_rate,port_path):
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, 
                            self.baud_rate, timeout=3.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            writeTimeout=3.0)

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
                            self.baud_rate, timeout=3.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            writeTimeout=3.0)
    
  def send_message(self,message):
    if self.ser.isOpen():
      self.ser.write(message)
 
  def receive_message(self):
    message = ""
    if self.ser.isOpen():
      message = self.ser.readline()
    return message.strip('\n')

  def clear_serial(self):
    self.ser.flushInput()
    self.ser.flushOutput()

  def remove_character(self,message,character):
    return message.strip(character)


