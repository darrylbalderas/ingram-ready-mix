import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep
from time import time

def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  try:

  except KeyboardInterrupt:
    print("\nexit")

if __name__ == "__main__":
  main()

