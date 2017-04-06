from charlie_test import *
from transceiver import Transceiver
from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor
from threading import Thread
from battery import Battery

if __name__ == "__main__":
  send_queue= []
  out_queue = []
  tri_queue = []
  rain_queue = []
  port = xbee_usb_port()
  if port != None:
    try:
      charlie_xbee = Transceiver(9600,port,out_queue,tri_queue,rain_queue,send_queue)
      rain_guage = RainGuage(rain_guage_pin,30)
      flow_sensor = FlowSensor(flow_sensor_pin)
      level_sensor = LevelSensor() 
      battery = Battery()
      thread1 = Thread(target = detect_rainfall, args = (rain_guage,level_sensor,tri_queue,rain,queue,
                       send_queue,battery,))
      thread1.start()
      thread2 = Thread(target = transmission, args =(charlie_xbee,))
      thread2.start()
      detect_outfall(flow_sensor,level_sensor,out_queue,send_queue)
    except KeyboardInterrupt:
      print("Ending the program")
      thread1.join()
      thread2.join()
  else:
    print("Missing xbee device")
