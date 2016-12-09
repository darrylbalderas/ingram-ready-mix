import serial
import glob
import sys
import requests
from xbee import XBee
from xbee import frame

system_name = sys.platform

class Transmitter:
  def __init__(self, baudRate, xbee_id):
    self.port_Number = self.xbee_Usb_Port()
    self.baudRate = baudRate
    self.connection = serial.Serial(self.port_Number, baudRate, timeout=0.5)
    self.id = xbee_id
    self.xb = XBee(self.connection)

  def stopUsbConnection(self):
    self.xb.halt()
    self.connection.close()
    
  def resetUsbConnection(self):
    self.xb.halt()
    self.connection.close()
    self.connection = serial(self.port_Number,self.baudRate, timeout =0.5)

  def readXbeeData(self):
    self.xb.wait_read_frame()
    
  def establishXbeeConnection(self):
    print("Function Not Done")
    
  def xbee_Usb_Port(self):
      ports = glob.glob('/dev/tty[A-Za-z]*')
      result = []
      for port in ports:
          try:
              s = serial.Serial(port)
              s.close()
              result.append(port)
          except( OSError, serial.SerialException):
              pass
      return result[0]



xb = Transmitter(9600,1)
port = xb.xbee_Usb_Port()


