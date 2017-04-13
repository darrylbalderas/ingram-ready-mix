from time import time
import RPi.GPIO as gpio

restart_button_pin = 8
gpio.setmode(gpio.BOARD)
gpio.setup(restart_button_pin,gpio.IN)

def check_restart():
	return gpio.input(restart_button_pin)


def main():
	while True:
		try:
			if check_restart():
				previous_time = time()
				while time()-previous_time <=  3:
					if check_restart():
						print("Restart button has been pressed for %f"%(time()-previous_time))
					else:
						break
		except:
			gpio.cleanup()

if __name__ == "__main__":
	main()



