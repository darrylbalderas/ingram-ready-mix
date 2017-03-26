import serial
import glob
import sys
from time import sleep
import Queue

'''
This Transmitter class was created for the sole purpose 
of testing our Xbee modules. In our senior design project,
the role of transmitter will be assigned to Team Charlie
since we have to wait for their signal to invoke our functionality
'''
class Job(object):
    def __init__(self, priority, message):
        self.priority = priority
        self.description = message
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

class Transceiver:
  def __init__(self, baud_rate,port_path, receive_queue, send_queue):
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, 
                            self.baud_rate, timeout=2.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    self.receive_queue = receive_queue
    self.send_queue = send_queue

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
                            self.baud_rate, timeout=1.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBIT)
    
  def send_message(self):
    message = ""
    if self.ser.isOpen():
      if not self.send_queue.empty():
        print("trying sending message")
        job =  self.send_queue.get()
        message = job.description + "\n"
        self.ser.write(message)
        self.flush_output()
      else:
        print("send queue empty")
 
  def receive_message(self):
    message = ""
    if self.ser.isOpen():
      try:
        message = self.ser.readline()
        if message == "":
          print("empty message")
        self.flush_input() 
        message = message.strip('\n')
        if message != "" and len(message) >= 3:
          if message == "out" or message == "oyes":
            self.receive_queue.put(Job(1,message))
          elif message == "tri" or message == "tyes" or message == "ryes":
            self.receive_queue.put(Job(2,message))
          else:
            self.receive_queue.put(Job(3,message))
      except:
        pass

  def flush_input(self):
    sleep(0.5)
    self.ser.flushInput()
    sleep(0.5)

  def flush_output(self):
    sleep(0.5)
    self.ser.flushOutput()
    sleep(0.5)


