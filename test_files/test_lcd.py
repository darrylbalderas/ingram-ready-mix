from lcd import LCD
import glob
from time import sleep

def lcd_serial_port():
  '''
  Paramter: None
  Function: Looks for the port used by the 16x2 LCD screen
  Returns: port used 16x2 screen port
  '''
  port =  glob.glob('/dev/ttyACM*')
  #port = glob.glob('/dev/tty.usb*')
  if len(port) != 0:
    return port[0]
  else:
    return None


def main():
	port = lcd_serial_port()
	if port != None:
		lcd = LCD(port, 9600)
##		lcd.welcome_message()
##		sleep(5)
##		lcd.complete_message()
##		sleep(5)
##		lcd.missed_message()
##		sleep(5)
##		lcd.holding_restart(3)
##		sleep(5)
##		lcd.restart_message()
##		sleep(5)
		lcd.display_timer(0)
		sleep(5)
##		lcd.display_voltage(12.0,30,'complete',False)
##		sleep(5)
##		lcd.send_command('CLEAR')
##		lcd.display_voltage(12.0,12,'missed',False)
##		sleep(5)
##		lcd.send_command('CLEAR')
##		lcd.display_voltage(12.0,'None','None',False)
##		sleep(5)
##		lcd.send_command('CLEAR')		
##		lcd.display_voltage(2.0,30,'complete',True)
##		sleep(5)
##		lcd.send_command('CLEAR')		
##		lcd.display_voltage(2.0,12,'missed',True)
##		sleep(5)
##		lcd.send_command('CLEAR')
##		lcd.display_voltage(2.0,'None','None',True)
##		sleep(5)
##		lcd.send_command('CLEAR')


	else:
		print("Missing LCD screen")

if __name__ == "__main__":
	main()
