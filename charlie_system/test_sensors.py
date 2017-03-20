from flow_sensor import FlowSensor
from rain_guage import RainGuage
from level_sensor import LevelSensor
from charlie_test import *

def main():
        rain_guage = RainGuage(rain_guage_pin,30)
        flow_sensor = FlowSensor(flow_sensor_pin)
        level_sensor = LevelSensor()
        while True:
                try:
                        print("printing the sensor values")
                        print("The value of the Rain Guage is: %f" %(rain_guage.get_total_rainfall()))
                        print("The value of the flow sensor is: %d" %(flow_sensor.check_flow()))
                        print("The value of the level_sensor is: %d\n" %(level_sensor.get_pool_level()))
                except KeyboardInterrupt:
                        print("\nExiting the program")


if __name__ == "__main__":
	main()
