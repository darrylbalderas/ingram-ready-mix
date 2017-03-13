import glob 
import sys
from time import sleep
import RPi.GPIO as GPIO

class LevelSensor:
	def __init__(self,pin):
		self.pin = pin
		self.floor_rating = -0.10
		self.ceiling_rating = 0.10
		self.pool_level = 12
		self.floor_level = 2190
		self.ceiling_level = 2200

	def check_level_sensor(self):
		return GPIO.input(self.pin)

	def resistance_to_inches(self):
		inches_left = 12
		#Between 0 to 1 inches filled on tap
		if self.floor_level >= 2190 and self.ceiling_level <= 2200:     
			inches_left = 12
		#Between 1 to 2 inches filled on tape
	    elif self.floor_level  >= 2020 and self.ceiling_level <= 2189:   
			inches_left = 11
		#Between 2 to 3 inches filled on tape
	    elif self.floor_level  >= 1890 and self.ceiling_level <= 2019:   
		    inches_left = 10
		#Between 3 to 4 inches filled on tape
	    elif self.floor_level  >= 1710 and self.ceiling_level <= 1889:  
		    inches_left = 9
		#Between 4 to 5 inches filled on tape
	    elif self.floor_level  >= 1550 and self.ceiling_level <= 1709:   
		    inches_left = 8
		#Between 5 to 6 inches filled on tape
	    elif self.floor_level  >= 1390 and self.ceiling_level <= 1549:  
		    inches_left = 7
		#Between 6 to 7 inches filled on tape
	    elif self.floor_level  >= 1220 and self.ceiling_level <= 1389:  
		    inches_left = 6
		#Between 7 to 8 inches filled on tape
	    elif self.floor_level  >= 1080 and self.ceiling_level <= 1219:   
		    inches_left = 5
		#Between 8 to 9 inches filled on tape
	    elif self.floor_level  >= 910 and self.ceiling_level <= 1079:    
		    inches_left = 4
		#Between 9 to 10 inches filled on tape
	    elif self.floor_level  >= 770 and self.ceiling_level <= 909:
		    inches_left = 3
		#Between 10 to 11 inches filled on tape
	    elif self.floor_level  >= 610 and self.ceiling_level <= 769:     
		    inches_left = 2
		#Between 11 to 12 inches filled on taped
	    elif self.floor_level  >= 420 and self.ceiling_level <= 609:     
		    inches_left = 1
		#Between 12 inches filled on taped
	    elif self.floor_level  >= 380 and self.ceiling_level <= 419:
		    inches_left = 0

		return inches_left

	def get_pool_level(self):
	    #eTape Continuous Fluid Level PN-12110215TC-12
	    #Sensor Output: 2250ohms empty, 400 ohms full +- 10%
	    data = self.check_level_sensor()
	    self.floor_level = data + (data * self.floor_rating)
	    self.ceiling_level = data + (data * self.ceiling_rating)
	    self.pool_level = resistance_to_inches()
	      
	    #Create the rules here to see the amount of inches needed for outfall
	    #pool_level equals the amount left for outfall to occur
	    return self.pool_level

	def check_overflow(self):
		if self.pool_level == 0:
			return True
		else:
			return False





