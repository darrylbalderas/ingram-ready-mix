#sudo apt-get update
#sudo apt-get install sense-hat
#sudo reboot

#documentation can be found under this directory 
#/usr/src/sense-hat/examples
#After looking at the documenation we should copy the documetation to our github folder
#cp /usr/src/sense-hat/examples <github folder directory> -a

# Here is the website to the documentation to the senseHat module --->  https://pythonhosted.org/sense-hat/
# If you want to check more functionality for the senseHat module look at this git repo --> https://github.com/RPi-Distro/python-sense-hat 
# After completing the steps this is a program that will test the functionality of the raspberry pi 

from sense_hat import SenseHat
import xbee
import os
import time
import sys 
import math


sense = SenseHat()
sense.clear()

#pixels would be the color we would like to send 

#sense.set_pixels(pixels)
sense.show_message("Hello world!")

print "1"
