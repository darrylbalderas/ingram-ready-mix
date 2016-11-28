from sense_hat import SenseHat
import os
import time import sleep
import math
import sys

class LedMatrix:
  def __init__(self):
    self.sense_hat = SenseHat()
    self.colors = {'r' : [ 255,0,0 ] , 
                   'y' : [ 255, 135, 0], 
                   'b':  [ 0,0,255], 
                   'g' : [ 0, 255, 0],
                   'v' : [159,0,255] 
                   'w' : [0,0,0]
                  }
    self.color_images = { 'red' : self.make_Image(self.colors['r'])
                    'yellow' : self.make_Image(self.colors['y'])
                    'green' : self.make_Image(self.colors['g'])
                    'violet' : self.make_Image(self.colors['v'])
                    'blue' : self.make_Image(self.colors['b'])
                    'white' : self.make_Image(self.colors['w'])  
                  } 
    self.row = 8
    self.column = 8
    
##These are the different type of colors 
  def make_Image(color):
      image = [] 
      for i in range(self.row*self.column):
          image.append(color)
      return image
    
  def change_Color(self,color_image):
    self.sense_hat.set_pixels(color_image)
    
  def change_color_Row(self,color_image,new_color,row):
    multiple = 8 
    start = (row-1) * multiple 
    end = (row*multiple)
    for i in range(start,end):
      color_Image[i] = new_color
    self.sense_hat.set_pixels(color_image)
    
  def clear_Matrix(self):
    self.sense_hat.clear()

  def get_colors():
    return self.colors

  def set_colors(colors):
    self.colors = colors

  def get_colorImage():
    self.color_image
    
  def set_colorImage(color_image):
    self.color_image = color_image

      
   
