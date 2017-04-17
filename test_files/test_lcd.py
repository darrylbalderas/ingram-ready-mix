from lcd import LCD
import glob

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
		lcd.test_message()
	else:
		print("Missing LCD screen")

if __name__ == "__main__":
	main()
