import charlie_test as implement
from transceiver import Transceiver
from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor
from threading import Thread
from threading import Event
from battery import Battery


def main():
  pin_dictionary = implement.get_pins()
  event = Event()
  implement.initialize_files()
  sender_queue= []
  out_queue = []
  trigger_queue = []
  rain_queue = []
  port = implement.xbee_usb_port()
  if port != None:
    charlie_xbee = Transceiver(9600,port,out_queue,trigger_queue,rain_queue,sender_queue)
    rain_guage = RainGuage(pin_dictionary['rain'],30)
    flow_sensor = FlowSensor(pin_dictionary['flow'])
    level_sensor = LevelSensor()
    battery = Battery()
    thread1 = Thread(target = implement.detect_rainfall, args = (rain_guage,level_sensor,trigger_queue,rain_queue,
                     sender_queue,battery,event,))
    thread1.start()
    thread2 = Thread(target = implement.transmission, args =(charlie_xbee,event,))
    thread2.start()
    thread3 = Thread(target = implement.detect_outfall, args=(flow_sensor,level_sensor,out_queue,sender_queue,event,))
    thread3.start()
    while not event.is_set():
      user_input = raw_input("Enter Y or N for stopping Threads")
      if user_input.lower() == 'y':
        event.set()
        thread1.join()
        thread2.join()
        thread3.join()
  else:
    print("Missing xbee device")


if __name__ == "__main__":
  main()
