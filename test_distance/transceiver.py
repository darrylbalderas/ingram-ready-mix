'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the Xbee hardware
'''
import serial
from time import sleep

class Transceiver:
  def __init__(self, baud_rate,port_path, receiver_queue,sender_queue):
    '''
    Parameters: Baudrate(integer), port_path(string), out_queue(list used for flow_sensor triggers),
    trigger_queue (list for rain_guage triggers), rain_queue (list for rainfall and pool level data),
    voltage_queue ( list for voltages), sender_queue (list for sending information)
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
    self.receiver_queue = receiver_queue

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
        sleep(0.25)
 
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
        # self.flush_input()
        message = message.strip('\n')
        if message != "" and len(message) >= 2:
            if message == "hey":
                if not message in self.receiver_queue:
                    self.receiver_queue.append(message)
      except:
        pass

  def flush_input(self):
    sleep(0.1)
    self.ser.flushInput()
    sleep(0.1)

  def flush_output(self):
    sleep(0.1)
    self.ser.flushOutput()
    sleep(0.1)


