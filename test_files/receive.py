
import sys 
import glob
import serial 
from transceiver import transceiver


def xbee_usb_port():
  if sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')
  elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  if len(ports) != 0:
      result = []
      for port in ports:
          try:
              ser = serial.Serial(port)
              ser.close()
              result.append(port)
          except( OSError, serial.SerialException):
              pass
      return result[0]
  else:
      return None


def main():
  send_queue= [ ]
  out_queue = [ ]
  trigger_queue = [ ]
  data_queue = [ ]
  voltage_queue = [ ]
  bt.initialize_files()
  xbee_port = bt.xbee_usb_port()

  if xbee_port != None:
    pass
  else:
    print("No Xbee connected")