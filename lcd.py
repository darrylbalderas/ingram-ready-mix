import serial 
import sys
import glob
from time import sleep

class LCD:
  def __init__(self,lcd_port,baudrate):
    self.ser = serial.Serial(lcd_port,baudrate,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)

    self.commands = {'TURN_OFF' : b'\xFE\x46'
                    ,'TURN_ON' :b'\xFE\x42'
                    ,'AUTOSCROLL_ON' : b'\xFE\x51'
                    ,'AUTOSCROLL_OFF' : b'\xFE\x52'
                    ,'CLEAR' : b'\xFE\x58'
                    ,'START_UP' : b'\xFE\x40'
                    ,'BACKSPACE' :b'\x08'
                    ,'ENTER' : b'\x0D'
                    ,'NEW_LINE' : b'\x0A'
                    ,'BACKLIGHT_RED' : b'\xFE\xD0\xFF\x00\x00'
                    ,'BACKLIGHT_WHITE': b'\xFE\xD0\xFF\xFF\xFF'
                    ,'BACKLIGHT_BLUE': b'\xFE\xD0\x00\x00\xFF'
                    ,'SET_BACKLIGHT': b'\xFE\xD0'
                    ,'MOVE_CURSOR' : b'\xFE\x4D'
                    ,'BACK_CURSOR': b'\xFE\x4C'
                    ,'HOME': b'\xFE\x48'
                    ,'ON_CURSOR': b'\xFE\x53'
                    ,'OFF_CURSOR': b'\xFE\x54'}

    if self.ser.isOpen():
      self.ser.write(self.commands['CLEAR'])
      self.ser.write(self.commands['AUTOSCROLL_OFF'])
      
  def send_command(self,command):
    if self.ser.isOpen():
        self.ser.write(self.commands[command])
        usleep(1)

  def send_message(self,message):
    if self.ser.isOpen():
        self.ser.write(message)
        usleep(1)


def usleep(seconds):
    number = seconds/float(1000)
    sleep(number)


