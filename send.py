import sys
import glob 
import serial
from transceiver import Transceiver
from time import sleep
from time import time

def check_status():
  char_input = ""
  while char_input != 'y':
    char_input = raw_input("Trigger the rain guage: ")


def main():
  port = xbee_usb_port()
  xbee = Transceiver(9600,port)
  try:
    check_status()
    create_trigger(xbee)
    send_data(xbee)
  except KeyboardInterrupt:
    print("\nexit")

if __name__ == "__main__":
  main()

