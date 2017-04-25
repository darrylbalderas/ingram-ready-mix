import RPi.GPIO as gpio
from time import sleep
from ledmatrix import LedMatrix
from lcd import LCD
import glob 
from time import time

complete = 12
buzzers = [4,17,27,22,6,13]

def check_complete():
  '''
  Parameters: None
  Function: Checks whether the gpio pin for complete button has
  been pressed resulting in the status either a 1 or 0
  Returns: The status of the complete button
  '''
  return gpio.input(complete)

def lcd_serial_port():
  '''
  Paramter: None
  Function: Looks for the port used by the 16x2 LCD screen
  Returns: port used 16x2 screen port
  '''
  port =  glob.glob('/dev/ttyACM*')
  if len(port) != 0:
    return port[0]
  else:
    return None

def initalize_buzzers():
  '''
  Parameters: None
  Function: Initializes the pins used by the buzzers as output
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.setup(buzzer,gpio.OUT)

def start_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending
  a boolean value True in order to turn on
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.output(buzzer,True)

def stop_buzzer():
  '''
  Parameters: None
  Function: Invokes all of the pins used by the buzzers by sending 
  a boolean value False in order to turn off
  Returns: None
  '''
  for buzzer in buzzers:
    gpio.output(buzzer,False)

def main():
  gpio.setmode(gpio.BCM) 
  gpio.setup(complete,gpio.IN)
  initalize_buzzers()
  led_matrix = LedMatrix()
  port = lcd_serial_port()
  lcd = LCD(port,9600)
  flag = False
  while not flag:
    user_input = raw_input("Enter (Y) to invoke system: ")
    if user_input.lower() == "y":
      start_time = time()
      start_buzzer()
      led_matrix.change_color(led_matrix.get_blueImage())
      while time()-start_time < 900:
        lcd.display_timer(time()-start_time)
        if check_complete():
          flag = True
          stop_buzzer()
          gpio.cleanup()
          lcd.send_command('CLEAR')
          led_matrix.clear_matrix()

main()
