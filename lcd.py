import serial 
from time import sleep
from math import floor

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

  def bappend_blanks(self,message):
    '''
    appends blanks spaces at the end of the message
    '''
    if len(message) != 16:
        blanks = 16 - len(message)
        return (blanks*" " + message)

  def center_message(self,message):
    '''
    appends blanks spaces in order to center the message
    '''
    length = len(message)
    if length < 16 and length > 0:
        blanks = int(floor((16 - length)/2))
        return (blanks*" " + message)

  def welcome_message(self):
    '''
    creates a default message to 
    '''
    self.send_command('CLEAR')
    self.send_message(self.center_message('Welcome to'))
    self.send_command('ENTER')
    self.send_message(self.center_message("IngramReady Mix"))
    # lcd.send_message(self.center_message("Mix\r"))
    sleep(5)
    self.send_command('CLEAR')

  def waiting_message(self,message):
    self.send_message(self.center_message("waiting on"))
    self.send_command('ENTER')
    self.send_message(self.center_message(message +"..."))
    self.send_command('HOME')

  def complete_message(self):
    self.send_command('CLEAR')
    self.send_message(self.center_message('completed'))
    self.send_command('ENTER')
    self.send_message(self.center_message('sample'))
    sleep(5)
    self.send_command('CLEAR')
    self.send_message(self.center_message("sleep for rest"))
    self.send_command('ENTER')
    self.send_message(self.center_message("of the month"))
    sleep(5)
    self.send_command('CLEAR')

  def missed_message(self):
    self.send_command('CLEAR')
    self.send_message(self.center_message(' missed'))
    self.send_command('ENTER')
    self.send_message(self.center_message('sample'))
    sleep(5)
    self.send_command('CLEAR')
    self.send_message(self.center_message("sleep for rest"))
    self.send_command('ENTER')
    self.send_message(self.center_message("of the day"))
    sleep(5)
    self.send_command('CLEAR')

  def holding_restart(self,num_time):
    self.send_message(self.center_message("RESTART HOLD"))
    self.send_command('ENTER')
    seconds = str(int(3-floor(num_time)%3)).zfill(2)
    self.send_message(self.center_message(seconds))
    self.send_command('HOME')

  def restart_message(self):
    self.send_command('CLEAR')
    self.send_message(self.center_message("Restarting"))
    self.send_command('ENTER')
    self.send_message(self.center_message('System'))
    sleep(2)
    self.send_command('CLEAR')

  def display_timer(self,num_time):
    hour = str(int(floor(num_time/3600))).zfill(2)
    minute = str(int(14- floor(num_time/60))).zfill(2)
    seconds =  str(int(59 - floor(num_time))%60).zfill(2)
    # time_m = "{0:.3f}\r".format(num_time)
    time_m = "%s:%s:%s"%(hour,minute,seconds)
    self.send_message(self.center_message('Timer'))
    self.send_command('ENTER')
    self.send_message(self.center_message(time_m))
    self.send_command("HOME")

  def display_days(self,num_days):
    self.send_message(self.center_message('Days left'))
    self.send_command('ENTER')
    self.send_message(self.center_message(str(num_days)))
    self.send_command("HOME")

  def display_hour(self,num_hours):
    self.send_message(self.center_message('Hrs left'))
    self.send_command('ENTER')
    self.send_message(self.center_message(str(num_hours)))
    self.send_command("HOME")

def usleep(seconds):
    number = seconds/float(1000)
    sleep(number)



