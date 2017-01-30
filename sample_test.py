import sys
import RPi.GPIO as gpio
from time import sleep
import glob
import serial
from transceiver import Transceiver
from lcd import LCD
from buzzer import Buzzer
from ledmatrix import LedMatrix
from time import time

buzzers = [4,17,22,5,6,13]
reset = 21
yellow = [255,135,0]
green = [0,255,0]
red = [255,0,0]
gpio.setmode(gpio.BCM)
gpio.setup(reset,gpio.IN)

miss_message="missed sample   "
complete_message = "complete sample "
restart_message = "Restart system  "

comm_message = "Comm establish  "
nocomm_message = "NoComm establish"


def check_reset():
  return not gpio.input(reset)

def initalize_buzzers(buzzers):
  for buzzer in buzzers:
    gpio.setup(buzzer,gpio.OUT)

def start_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,True)

def stop_buzzer():
  for buzzer in buzzers:
    gpio.output(buzzer,False)

  
def lcd_serial_port():
  port =  glob.glob('/dev/ttyACM*')
  return port[0]

def xbee_usb_port():
  '''
  Search in your file directory to find Usb port 
  that your Xbee is connected to. Supports MacOs and 
  linux operating system. Returns a list of usb ports. 
  '''
  result = []
  if sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usbserial*')
  elif sys.platform.startswith('linux'):
    ports = glob.glob('/dev/ttyU*')

  for port in ports:
      try:
          ser = serial.Serial(port)
          ser.close()
          result.append(port)
      except( OSError, serial.SerialException):
          pass
  return result[0]

def make_newcolor(color):
  image = []
  for i in range(64):
    if color.lower() == "yellow":
      image.append(yellow)
    elif color.lower() == "red":
      image.append(red)
    elif color.lower() == "green":
      image.append(green)
  return image
    

def invoke_system(led_matrix,color_array, colors,lcd):
  invoke_color = make_newcolor("yellow")
  led_matrix.clear_matrix()
  led_matrix.change_color(invoke_color)
  start_buzzer()
  row_duration  = 1.875*2
  count_row = 1
  max_time = 15*2
  previous_time = time()
  current_time = 0
  timer = ""
  while current_time <= max_time:
    if check_reset():
      lcd.send_command("CLEAR")
      sleep(0.5)
      lcd.send_message(complete_message)
      count_row = 1
      reset_button(led_matrix,color_array)
      break
    
    current_time = time() - previous_time
    timer = "{0:.4f}".format(current_time)
    blank_spaces = 16 - len(timer)
    message = timer + blank_spaces*" "
    lcd.send_message(message)
    if current_time >= row_duration*count_row:
          print current_time
          print row_duration*count_row
          color_image = led_matrix.change_color_row(invoke_color,colors[1], count_row)
          count_row += 1

  if count_row >= 8:
    missed_button(led_matrix,color_array)
    sleep(0.5)
    lcd.send_command("CLEAR")
    sleep(1)
    lcd.send_message(miss_message)
    sleep(2)
    lcd.send_message("sleep rest day  ")
    sleep(3)
    lcd.send_message("ready           ")
    reset_button(led_matrix,color_array)

  

def reset_button(led_matrix,color_array):
  led_matrix.clear_matrix()
  led_matrix.change_color(color_array[0])
  stop_buzzer()

def missed_button(led_matrix, color_array):
  led_matrix.clear_matrix()
  led_matrix.change_color(color_array[1])
  stop_buzzer()

def main():
  initalize_buzzers(buzzers)
  xbee_port = xbee_usb_port()
  lcd_port = lcd_serial_port()
  lcd = LCD(lcd_port,9600)
  bravo_xbee = Transceiver(9600,xbee_port,b"\x00\x13\xA2\x00\x41\x04\x96\x6E")
  led_matrix = LedMatrix()
  
  color_images = led_matrix.get_color_images()
  color_info = led_matrix.get_colors()
  color_array = [color_images['green'], color_images['red'], color_images['yellow']]
  colors = [color_info['g'], color_info['r'], color_info['y']]
  lcd.send_message(nocomm_message)
  led_matrix.change_color(color_array[0])
  while True:
    try:      
      message = bravo_xbee.receive_message()
      if message == "b":
        for i in range(10):
          xbee.write("a")
        lcd.send_command("CLEAR")
        sleep(0.5)
        lcd.send_message(comm_message)
        sleep(2)
        invoke_system(led_matrix,color_array,colors,lcd)
      
    except KeyboardInterrupt:
      lcd.send_command("CLEAR")
      led_matrix.clear_matrix()
      stop_buzzer()
      gpio.cleanup()
      break

##def sample():
##  led_matrix = LedMatrix()
##  color_images = led_matrix.get_color_images()
##  color_info = led_matrix.get_colors()
##  color_array = [color_images['green'], color_images['red'], color_images['yellow']]
##  colors = [color_info['g'], color_info['r'], color_info['y']]
##
##  while True:
##    led_matrix.change_color(color_array[0])
##    sleep(2)
##    led_matrix.clear_matrix()
##    led_matrix.change_color(color_array[1])
##    sleep(2)
##    led_matrix.clear_matrix()
##    led_matrix.change_color(color_array[2])
##    sleep(2)
##    led_matrix.clear_matrix()

  

if __name__ == '__main__':
  main()
