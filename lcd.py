'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the 16x2 lcd screen
'''

import serial 
from time import sleep
from math import floor

class LCD:
  def __init__(self,lcd_port,baudrate):
    '''
    Parameters: lcd_port (string), baudrate (integer)
    Function: Initializes variables when an instance
    of a 16x2 LCD screen object. 
    Creates a list of commands used by 
    lcd object.  Clears and turn offs
    autoscroll off.
    Returns: None
    '''
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
    '''
    Parameters: command(string)
    Function: Writes a command to the 16x2 LCD screen
    Returns: None
    '''
    if self.ser.isOpen():
        self.ser.write(self.commands[command])
        msleep(1)

  def send_message(self,message):
    '''
    Parameters: message(string)
    Function: Writes a message to the 16x2 LCD screen
    Returns: None
    '''
    if self.ser.isOpen():
        self.ser.write(message)
        msleep(1)

  def bappend_blanks(self,message):
    '''
    Parameters: message(string)
    Function: appends a certain blanks to end of the message
    Returns: message with blanks appended to it 
    '''
    if len(message) != 16:
        blanks = 16 - len(message)
        return (blanks*" " + message)

  def center_message(self,message):
    '''
    Parameters: message(string)
    Function: appends blanks characters to center the message in 
    the lcd screen
    Returns: a message that will be centered in the lcd screen
    '''
    length = len(message)
    if length < 16 and length > 0:
        blanks = int(floor((16 - length)/2))
        return (blanks*" " + message)

  def welcome_message(self):
    '''
    Parameters: None
    Function: displays a welcome message on 16x2 lcd screen
    Returns: None
    '''
    self.send_command('CLEAR')
    self.send_message(self.center_message('Welcome to'))
    self.send_command('ENTER')
    self.send_message(self.center_message("IngramReady Mix"))
    sleep(3)
    self.send_command('CLEAR')

  def complete_message(self):
    '''
    Parameters: None
    Function: displays a message on the 16x2 lcd screen whenever 
    the user has pressed the complete button 
    Returns: None
    '''
    self.send_command('CLEAR')
    self.send_message(self.center_message('completed'))
    self.send_command('ENTER')
    self.send_message(self.center_message('sample'))
    sleep(3)
    self.send_command('CLEAR')
    self.send_message(self.center_message("sleep for rest"))
    self.send_command('ENTER')
    self.send_message(self.center_message("of the month"))
    sleep(3)
    self.send_command('CLEAR')

  def missed_message(self):
    '''
    Parameters: None
    Function: displays a message on the 16x2 lcd screen whenever the 
    user has pressed the missed button
    Returns: None
    '''
    self.send_command('CLEAR')
    self.send_message(self.center_message(' missed'))
    self.send_command('ENTER')
    self.send_message(self.center_message('sample'))
    sleep(3)
    self.send_command('CLEAR')
    self.send_message(self.center_message("sleep for rest"))
    self.send_command('ENTER')
    self.send_message(self.center_message("of the day"))
    sleep(3)
    self.send_command('CLEAR')

  def holding_restart(self,num_time):
    '''
    Parameters: None
    Function: displays a counted down message on the 16x2 lcd 
    screen whenever the user is pressing the restart button
    Returns: None
    '''
    self.send_message(self.center_message("Hld Restart Btn"))
    self.send_command('ENTER')
    seconds = int(3-floor(num_time)%3)
    if seconds == 1:
      value = str(seconds).zfill(2) + ' second'
    else:
      value = str(seconds).zfill(2) + ' seconds'
    self.send_message(self.center_message(value))
    self.send_command('HOME')

  def restart_message(self):
    '''
    Parameters: None
    Function: displays a message on the 16x2 lcd screen 
    whenever the user has pressed the restart message
    Returns: None
    '''
    self.send_command('CLEAR')
    self.send_message(self.center_message("Restarting"))
    self.send_command('ENTER')
    self.send_message(self.center_message('System'))
    sleep(2)
    self.send_command('CLEAR')

  def display_timer(self,num_time):
    '''
    Parameters: None
    Function: displays a counted timer on the 16x2 screen 
    whenever our system has been invoked to show how much time 
    left to collect the sample.
    Returns: None
    '''
    hour = str(int(floor(num_time/3600))).zfill(2)
    minute = str(int(14- floor(num_time/60))).zfill(2)
    seconds =  str(int(59 - floor(num_time))%60).zfill(2)
    time_m = "%sh:%sm:%ss"%(hour,minute,seconds)
    self.send_message(self.center_message('Timer'))
    self.send_command('ENTER')
    self.send_message(self.center_message(time_m))
    self.send_command("HOME")

  def display_voltage(self,voltage_level,time_left,status,voltage_flag):
    '''
    Parameters: None
    Function: displays a message on the 16x2 lcd screen whenever the user
    is waiting to collect a sample
    Returns: None
    '''
    if status == 'complete':
        self.send_message(self.center_message('Days left: ' + str(time_left)))
        self.send_command('ENTER')
        if voltage_flag == False:
          self.send_message(self.center_message('Voltage: ' + str(voltage_level)+'V'))
        else:
          self.send_message(self.center_message('Check RDS'))
        self.send_command("HOME")
    elif status == 'missed':
        self.send_message(self.center_message('Hours left: '+ str(time_left)))
        self.send_command('ENTER')
        if voltage_flag == False:
          self.send_message(self.center_message('Voltage: ' + str(voltage_level) + 'V'))
        else:
          self.send_message(self.center_message('Check RDS'))
        self.send_command("HOME")
    else:
        self.send_message(self.center_message('No outfall'))
        self.send_command('ENTER')
        if voltage_flag == False:
          self.send_message(self.center_message('Voltage: ' + str(voltage_level) + 'V'))
        else:
          self.send_message(self.center_message('Check RDS'))
        self.send_command("HOME")



def msleep(seconds):
    '''
    Parameters: seconds(integers)
    Function: changes seconds into miliseconds
    Returns: None
    '''
    number = seconds/float(1000)
    sleep(number)



