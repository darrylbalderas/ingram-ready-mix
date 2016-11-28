import pyowm
import time
import sys
import os
import math 

API_key = 'dada4f99c37259165cdd868ec597570a'
san_marcos_id = 4726491

class Weather:

	def __init__(self, city_id):
		self.owm = pyowm.OWM(API_key)
        self.observations = self.owm.weather_at_id(city_id)
        self.weather = self.owm.get_weather()
    
    def get_rain(self):
    	return self.weather.get_rain()

    def get_cloudCoverage(self):
    	return self.weather.get_clouds

    def get_windSpeed(self):
    	return self.weather.get_wind()['speed']

    def get_windDegree(self):
    	return self.weather.get_wind()['deg']

    def get_humidity(self):
    	return self.weather.get_humidity()

    def get_temperature(self):
    	return self.weather.get_temperature('fahrenheit')['temp']

    def get_maxTemperature(self):
    	return self.weather.get_temperature('fahrenheit')['temp_max']

    def get_minTemperature(self):
    	return self.weather.get_temperature('fahrenheit')['temp_min']

    def get_weatherStatus(self):
    	return self.weather.get_status()

    def get_detail_weatherStatus(self):
    	return self.weather.get_detailed_status()









	






