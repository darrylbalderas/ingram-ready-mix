import RPi.GPIO as gpio
import time
import Adafruit_ADS1x15

class Battery:
    def __init__(self):
        self.voltage_level = 12.0
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 2
        self.adc_pin = 1
        self.max_reading = 14

    def get_adc_voltage(self, voltage_level):
        voltage_reading = 12.0 # default voltage value
        upper_bound = 1367
        lower_bound = 0
        total_boundary = upper_bound - (lower_bound)
        if voltage_level > upper_bound:
            voltage_level = upper_bound
        elif voltage_level < lower_bound:
            voltage_level = lower_bound
        tolerance = round((lower_bound/float(total_boundary))*self.max_reading ,2)
        if voltage_level < 0:
            voltage_level = 0.0
        voltage_reading = round((voltage_level/float(total_boundary)) * self.max_reading , 2) - tolerance
        return voltage_reading

    def get_voltage_level(self):
        voltage_level = self.adc.read_adc(self.adc_pin, gain=self.GAIN)
        time.sleep(0.25)
        self.voltage_level = self.get_adc_voltage(voltage_level)
        return self.voltage_level


def main():
    battery = Battery()
    voltage_level = 0
    while True:
        voltage_level = battery.get_voltage_level()
        print("This is the reading for your Battery: %.2f Volts" %(voltage_level))
        print("\n")

if __name__ == "__main__":
    main()
