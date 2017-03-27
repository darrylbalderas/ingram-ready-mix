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
# class Job(object):
#     def __init__(self, priority, message):
#         self.priority = priority
#         self.description = message
#     def __cmp__(self, other):
#         return cmp(self.priority, other.priority)

class Transceiver:
  def __init__(self, baud_rate,port_path, out_queue,trigger_queue, data_queue, send_queue):
    self.port_path = port_path
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port_path, 
                            self.baud_rate, timeout=2.0, 
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    self.send_queue= send_queue
    self.out_queue = out_queue
    self.trigger_queue = trigger_queue
    self.data_queue = data_queue

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
      if len(self.send_queue) != 0:#not self.send_queue.empty():
        message =  self.send_queue.pop(0)#self.send_queue.get()
        message = message + "\n"
        # self.send_queue.task_done()
        self.ser.write(message)
        self.flush_output()
 
  def receive_message(self):
    message = ""
    if self.ser.isOpen():
      try:
        message = self.ser.readline()
        self.flush_input()
        message = message.strip('\n')
        if message != "" and len(message) >= 3:
          if message == "out" or message == "oyes":
            if not message in self.out_queue:
              self.out_queue.append(message)
            # self.out_queue.put(message)
          elif message == "tri" or message == "tyes" or message == "ryes":
            if not message in self.trigger_queue:
              self.trigger_queue.append(message)
            # self.trigger_queue.put(message)
          else:
            if not message in self.data_queue:
              self.data_queue.append(message)
            # self.data_queue.put(message)
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


