from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor
from charlie_test import *

def main():
	rain_guage = RainGuage(rain_guage_pin,30)
    flow_sensor = FlowSensor(flow_sensor_pin)
    level_sensor = LevelSensor(level_sensor_pin)
    while True:
    	try:
    		print(""rain_guage.get_tick())
    		print(flow_sensor.check_outfall())
    		print(level_sensor.get_pool_level())
    	except KeyboardInterrupt:
    		print("\nExiting the program")


if __name__ == "__main__":
	main()