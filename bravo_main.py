from transceiver import Transceiver
from lcd import LCD
from ledmatrix import LedMatrix
from threading import Thread
from event import Event
import bravo_test as implement


def main():
  event = Event()
  pin_dictionary = implement.get_pins()
  send_queue= []
  out_queue = []
  trigger_queue = []
  data_queue = []
  voltage_queue = []
  implement.initialize_files()
  xbee_port = implement.xbee_usb_port()
  lcd_port = implement.lcd_serial_port()
  if xbee_port != None and lcd_port != None:
    bravo_xbee = Transceiver(9600,xbee_port,out_queue,trigger_queue,data_queue,voltage_queue,send_queue)
    implement.initalize_buzzers(pin_dictionary['buzzers'])
    led_matrix = LedMatrix()
    lcd = LCD(lcd_port,9600)
    led_matrix.change_color(led_matrix.get_greenImage())
    lcd.welcome_message()
    thread1 = Thread(target=implement.outfall_detection, args=(lcd,led_matrix,out_queue,send_queue,event,))
    thread1.start()
    thread2 = Thread(target=implement.rain_detection, args=(trigger_queue,data_queue,voltage_queue,send_queue,event,))
    thread2.start()
    thread3 = Thread(target=implement.transmission, args = (bravo_xbee,event,))
    thread3.start()

    while not event.is_set():
      user_input = raw_input("Enter Y or N to stop program")

      if user_input.lower() == 'y':
            print("Ending the Program")
            event.set()
            thread1.join()
            thread2.join()
            thread3.join()
            implement.stop_buzzer()
            led_matrix.clear_matrix()
            bravo_xbee.clear_serial()
            lcd.send_command('CLEAR')
  else:
      print("Check the Xbee and LCD connection")
if __name__ == "__main__":
  main()
