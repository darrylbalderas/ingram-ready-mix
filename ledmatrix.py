from sense_hat import SenseHat
# from time import time,
# from time import sleep

class LedMatrix:
  def __init__(self):
    self.__sense_hat = SenseHat()
    
    self.__colors = {'r' : [255,0,0], 
                     'y' : [255,135,0], 
                     'b':  [ 0,0,255], 
                     'g' : [ 0,255,0],
                     'v' : [159,0,255],
                     'w' : [255,255,255]
                    }

    self.__row = 8
    self.__column = 8
    
    self.__color_images = {'red' : self.make_image('r'),
                          'yellow' : self.make_image('y'),
                          'green' : self.make_image('g'),
                          'violet' : self.make_image('v'),
                          'blue' : self.make_image('b'),
                          'white' : self.make_image('w')  
                        }
    self.__row_duration = 1.875*60
    self.__max_time = 60*15
    
  def make_image(self,color):
      image = [] 
      for i in range(self.__row*self.__column):
          image.append(self.__colors[color])
      return image
    
  def change_color(self,color_image):
    self.__sense_hat.set_pixels(color_image)
    
  def change_color_row(self,color_image,new_color,row):
    start = (row-1) * self.__row 
    end = (row*self.__row)
    for i in range(start,end):
      color_image[i] = new_color
    self.__sense_hat.set_pixels(color_image)
    return color_image
    
  def clear_matrix(self):
    self.__sense_hat.clear()

  def get_colors(self):
    return self.__colors

  def set_colors(self,colors):
    self.__colors = colors

  def get_color_images(self):
    return self.__color_images
    
  def set_color_images(self,color_images):
    self.__color_images = color_images

  def get_row_duration(self):
    return self.__row_duration

  def set_row_duration(self,new_row_duration):
    self.__row_duration = new_row_duration

  def get_max_time(self):
    return self.__max_time

  def set_max_time(self):
    return self.__max_time

  def show_message(self,message):
    return self.__sense_hat.show_message(message,text_colour = [255,255,255])

  def ingram_colors(self,color):
    yellow = [255,135,0]
    green = [0,255,0]
    red = [255,0,0]
    blue = [0,0,255]
    image = []
    for i in range(64):
      if color.lower() == "yellow":
        image.append(yellow)
      elif color.lower() == "red":
        image.append(red)
      elif color.lower() == "green":
        image.append(green)
      elif color.lower() == "blue":
        image.append(blue)
    return image

  def get_greenImage(self):
    return self.__color_images['green']

  def get_redImage(self):
    return self.__color_images['red']

  def get_yellowImage(self):
    return self.__color_images['yellow']

  def get_blueImage(self):
    return self.__color_images['blue']

  def get_blue(self):
    return self.__colors['b']

  def get_green(self):
    return self.__colors['g']

  def get_red(self):
    return self.__colors['r']

  def get_yellow(self):
    return self.__colors['y']
