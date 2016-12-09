import serial
import serial.tools.list_ports
import glob
import sys
from time import sleep 
import requests
from xbee import XBee
from time import sleep

#Sychronous mode
class Transmitter:
  def __init__(self, baudRate):
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

  def sendXbeeData(self,command,parameter):
    self.xb.at(command = command)

  def readXbeeData(self):
    return self.xb.wait_read_frame()

    
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
      
    response = self.xb.wait_read_frame()
    return response

    
  def xbee_Usb_Port(self):
    # Look for COM port that might have an XBee connected
    portfound = False
    ports = list(serial.tools.list_ports)
    for p in ports:
        # The SparkFun XBee Explorer USB board uses an FTDI chip as USB interface
        if "FTDIBUS" in p[2]:
            print "Found possible XBee on " + p[0]
            if not portfound:
                portfound = True
                portname = p[0]
                print "Using " + p[0] + " as XBee COM port."
            else:
                print "Ignoring this port, using the first one that was found."
     
    if portfound:
        ser = serial.Serial(portname, 9600)
    else:
        sys.exit("No serial port seems to have an XBee connected.")
      # if sys.platform.startswith('darwin'):
      #   ports = glob.glob('/dev/tty.usb*')
      # else:
      #   ports = glob.glob('/dev/tty[A-Za-z]*')
      # result = []
      # for port in ports:
      #     try:
      #         s = serial.Serial(port)
      #         s.close()
      #         result.append(port)
      #     except( OSError, serial.SerialException):
      #         pass
      # return result[0]



def message_received(data):
  print data


xb = Transmitter(9600,'A')
xb.sendXbeeData('ID')
sleep(100)
print xb.readXbeeData()


xb = Transmitter(9600)

xb.sendXbeeData('D1', '\x05')

print xb.readXbeeData()



