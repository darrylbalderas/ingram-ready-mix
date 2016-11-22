import serial
import glob
import sys
import requests

system_name = sys.platform
baud_Rate = 9600

class XBee:
  def __init__(self, baudRate, xbee_id, rainfall_xbee):
    self.connection = serialConnection
    self.id = xbee_id
    self.rainfallXbee = rainfall_xbee
    self.port_Number = self.xbee_Usb_Port()
    
  def stopUsbConnection(self):
    print "Function Not Done"
    
  def resetUsbConnection():
    print "Function Not Done"
    
  def showUsbData():
    print "Function Not Done"
    
  def establishXbeeConnection():
    print "Function Not Done"
    
  def stopXbeeConnection():
    print "Function Not Done"
  
  def resetUsbConnection():
    print "Function Not Done"
    

  def xbee_Usb_Port():
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

xbee_Bravo = serial.Serial(port_Name, baud_Rate, timeout=0.5)



