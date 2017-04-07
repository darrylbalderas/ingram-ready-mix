import serial
from time import sleep

'''
This Transmitter class was created for the sole purpose 
of testing our Xbee modules. In our senior design project,
the role of transmitter will be assigned to Team Charlie
since we have to wait for their signal to invoke our functionality
'''

class Transceiver:
  def __init__(self, baud_rate,port_path, out_queue,trigger_queue, rain_queue,voltage_queue,sender_queue):
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
    self.voltage_queue = voltage_queue

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
      if len(self.sender_queue) != 0:
        message =  self.sender_queue.pop(0)
        message = message + "\n"
        self.ser.write(message)
        sleep(0.5)
 
  def receive_message(self):
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
            if not message in self.trigger_queue:
              self.trigger_queue.append(message)
          elif message == 'vyes' or message == 'vol' or message[0] == 'v':
            if not message in self.voltage_queue:
              self.voltage_queue.append(message)
          elif message[0] == 'r' or message[0] == 'p' or message == "ryes":
            if not message in self.rain_queue:
              self.rain_queue.append(message)
      except:
        pass

  def flush_input(self):
    sleep(0.25)
    self.ser.flushInput()
    sleep(0.25)

  def flush_output(self):
    sleep(0.25)
    self.ser.flushOutput()
    sleep(0.25)


