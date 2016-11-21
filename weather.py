import pyowm
import time
import sys
import os
import math 

API_key = 'dada4f99c37259165cdd868ec597570a'
owm = pyowm.OWM( API_key)
observations = owm.weather_at_id(4726491)
weather = observations.get_weather()


rain_volume = weather.get_rain()

if rain_volume != int:
	rain_volume = 0

cloud_coverage = weather.get_clouds()

if cloud_coverage != int:
	cloud_coverage = 0


wind_speed = weather.get_wind()['speed']
wind_degree = weather.get_wind()['deg']
humidity = weather.get_humidity()
temperature = weather.get_temperature('fahrenheit')['temp']
temp_max = weather.get_temperature('fahrenheit')['temp_max']
temp_min = weather.get_temperature('fahrenheit')['temp_min']
weather_short_status = weather.get_status()
weather_status = weather.get_detailed_status()

print "San marcos weather information"
print "------------------------------"

print "Rain Volume", rain_volume 

print "Cloud Coverage: ", cloud_coverage

print "Wind speed: ", wind_speed

print "Wind_degree: ", wind_degree

print "Humidity: ", humidity

print "Temperature: ", temperature

print "\tMax Temperature: ", temp_max
print "\tMin Temperature: ", temp_min
print "Weather Status Report: ", weather_status
print "\t Status Report: ", weather_short_status







	






