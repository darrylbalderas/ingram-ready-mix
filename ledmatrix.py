from sense_hat import SenseHat
import os
import time import sleep
import math
import sys

class LedMatrix:
  def __init__(self):
    self.sense_Hat = SenseHat()
    self.colors = {'r' : [ 255,0,0 ] , 
                   'y' : [ 255, 135, 0], 
                   'b':  [ 0,0,255], 
                   'g' : [ 0, 255, 0],
                   'v' : [159,0,255] 
                   'w' : [0,0,0]
                  }
    self.color_Images = { 'red' : self.make_Image(self.colors['r'])
                    'yellow' : self.make_Image(self.colors['y'])
                    'green' : self.make_Image(self.colors['g'])
                    'violet' : self.make_Image(self.colors['v'])
                    'blue' : self.make_Image(self.colors['b'])
                    'white' : self.make_Image(self.colors['w'])  
                  } 
    self.row = 8
    self.row = 8
    
##These are the different type of colors 
  def make_Image(color):
      image = [] 
      for i in range(row*column):
          image.append(color)
      return image
    
  def change_Color(self,color_Image):
    self.sense_Hat.set_pixels(color_Image)
    
  def change_color_Row(self,color_Image,row, new_color):
    multiple = 8 
    start = (row-1) * multiple 
    end = (row*multiple)
    for i in range(start,end):
      color_Image[i] = new_color
    self.sense_Hat.set_pixels(color_Image)
    
  def clear_Matrix(self):
    self.sense_Hat.clear()
      
   
