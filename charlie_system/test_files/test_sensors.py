import test_battery as Battery
import test_rain as Rain
import test_level as Level
import test_flow as Flow
import RPi.GPIO as gpio

def main():
	restart_pin = 8
	flow_sensor_pin = 10
	rain_guage_pin = 12
	restart_hold = 3 #seconds
	rain_collection_period = 30 #minutes
	gpio.setmode(gpio.BOARD)
	gpio.setup(restart_pin,gpio.IN) 
	battery = Battery.Battery()
	flow = Flow.FlowSensor(flow_sensor_pin)
	level = Level.LevelSensor()
	rain = Rain.RainGuage(rain_guage_pin,rain_collection_period)
	rainfall = 0
	voltage_level = 0
	pool_level = 0
	num_ticks = 0
	while True:
		try:
			pool_level = level.get_pool_level()
			voltage_level = battery.get_voltage_level()
			if rain.get_tick():
				rainfall, num_ticks = rain.get_total_rainfall(restart_pin,restart_hold)
				print("%f inches of rainfall and %d number of ticks collected from rain guage"%(rainfall,num_ticks))
			else:
				print("%f inches of rainfall and %d number of ticks collected from rain guage"%(0.0,0))

			if flow.check_outfall() == 1:
				print("There is outfall being detected")
			else:
				print("There is no outfall being detected")

			print("This is the reading for your Battery: %f Volts" %(voltage_level))
			print("This is the reading for your Level Sensor: %f inches" %(pool_level))
			print("\n")
		except KeyboardInterrupt:
			gpio.clear()
			print("\n")
			print("Exiting programming")



if __name__ == "__main__":
	main()
