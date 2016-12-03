import serial
import glob
import sys
from time import sleep 
import requests
from xbee import XBee

#Sychronous mode
class Transmitter:
  def __init__(self, baudRate, dest_id):
    self.port_Number = self.xbee_Usb_Port()
    self.baudRate = baudRate
    self.connection = serial.Serial(self.port_Number, baudRate)
    self.xb = XBee(self.connection)
    self.dest_id = dest_id

  def stopUsbConnection(self):
    self.connection.close()
    
  def resetUsbConnection(self):
    self.connection.close()
    self.connection = serial(self.port_Number,self.baudRate)

  def sendXbeeData(self,command):
    self.xb.at(frame_id = self.dest_id, command = command)

  def readXbeeData(self):
    return self.xb.wait_read_frame()

    
  def xbee_Usb_Port(self):
      if sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usb*')
      else:
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


def message_received(data):
  print data

xb = Transmitter(9600,'A')

xb.sendXbeeData('ID')
sleep(1)
print xb.readXbeeData()


