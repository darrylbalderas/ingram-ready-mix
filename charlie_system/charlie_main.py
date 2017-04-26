import charlie_test as ct
from transceiver import Transceiver
from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor
from threading import Thread
from battery import Battery
import RPi.GPIO as gpio
from time import sleep

def main():
  pin_dictionary = ct.get_pins()
  ct.initialize_files()
  sender_queue= [ ]
  outfall_queue = [ ]
  trigger_queue = [ ]
  rain_queue = [ ]
  port = ct.xbee_usb_port()
  if port != None:
    charlie_xbee = Transceiver(9600,port,outfall_queue,trigger_queue,rain_queue,sender_queue)
    rain_guage = RainGuage(pin_dictionary['rain'], 30)
    flow_sensor = FlowSensor(pin_dictionary['flow'])
    level_sensor = LevelSensor()
    battery = Battery()
    for x in range(2):
      voltage = battery.get_voltage_level()
      sender_queue.append('v'+'%.2f'%(voltage))
    thread1 = Thread(target = ct.detect_rainfall, args = (rain_guage,level_sensor,trigger_queue,rain_queue,sender_queue,battery,))
    thread1.start()
    sleep(1)
    thread3 = Thread(target = ct.detect_outfall, args=(flow_sensor,level_sensor,outfall_queue,sender_queue,))
    thread3.start()
    sleep(1)
    ct.transmission(charlie_xbee)
  else:
    print("Missing xbee device")


if __name__ == "__main__":
  main()
