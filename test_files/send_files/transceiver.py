'''
Created by: Matthew Smith, Michael Rodriguez, and Darryl Balderas
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the Xbee hardware 
'''
import serial
from time import sleep

class Transceiver:
  def __init__(self, baud_rate,port_path, out_queue,trigger_queue,rain_queue,sender_queue):
    '''
    Parameters: Baudrate(integer), port_path(string), out_queue(list used for flow_sensor triggers),
    trigger_queue (list for rain_guage triggers), rain_queue (list for rainfall and pool level data),
    sender_queue (list for sending information)
    Function: Initializes variables when an instance of Transceiver is created
    Returns: None
    '''
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, 
                            self.baud_rate, timeout=1.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    self.sender_queue= sender_queue
    self.out_queue = out_queue
    self.trigger_queue = trigger_queue
    self.rain_queue = rain_queue

  def close_serial(self):
    '''
    Parameters: None
    Function: closes serail communication
    Returns: None
    '''
    self.ser.close()
    
  def reset_serial(self): 
    '''
    Parameters: None
    Function: Closes and creates a new serial communication
    Returns: None
    '''     
    self.ser.close()
    self.ser = serial.Serial(self.port_path, 
                            self.baud_rate, timeout=1.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBIT)
    
  def send_message(self):
    '''
    Parameters: None
    Function: Checks if there is items in the sender_queue
    and send them through xbee serial port and which is transfered
    through wireless communication to specific xbee 
    Returns: None
    '''
    message = ""
    if self.ser.isOpen():
      if len(self.sender_queue) != 0:
        message =  self.sender_queue.pop(0)
        message = message + "\n"
        self.ser.write(message)
        sleep(0.5)
 
  def receive_message(self):
    '''
    Parameters: None
    Function: Recevies message from Rainfall detection system's 
    Xbee and stores the message in the respective queue
    Returns: None
    '''
    message = ""
    if self.ser.isOpen():
      try:
        message = self.ser.readline()
        message = message.strip('\n')
        if message != "" and len(message) >= 3:
          if message == "out" or message == "oyes":
            if not message in self.out_queue:
              self.out_queue.append(message)
          elif message == "tri" or message == "tyes":
            self.trigger_queue.append(message)
          elif message[0] == 'r' or message[0] == 'p' or message == "ryes":
            self.rain_queue.append(message)
      except:
        pass



