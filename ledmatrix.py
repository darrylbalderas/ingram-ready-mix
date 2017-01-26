from sense_hat import SenseHat
from time import time,sleep

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
    self.__color_images = { 'red' : self.make_Image('r'),
                          'yellow' : self.make_Image('y'),
                          'green' : self.make_Image('g'),
                          'violet' : self.make_Image('v'),
                          'blue' : self.make_Image('b'),
                          'white' : self.make_Image('w')  
                        }
    
    self.__row_duration = 1.875*60
    self.__max_time = 60*15
    
##These are the different type of colors 
  def make_Image(self,color):
      image = [] 
      for i in range(self.__row*self.__column):
          image.append(self.__colors[color])
      return image
    
  def change_Color(self,color_image):
    self.__sense_hat.set_pixels(color_image)
    
  def change_color_row(self,color_image,new_color,row):
    multiple = 8 
    start = (row-1) * multiple 
    end = (row*multiple)
    for i in range(start,end):
      color_image[i] = new_color
    self.__sense_hat.set_pixels(color_image)
    return color_image
    
  def clear_Matrix(self):
    self.__sense_hat.clear()

  def get_colors(self):
    return self.__colors

  def set_colors(self,colors):
    self.__colors = colors

  def get_color_images(self):
    return self.__color_images
    
  def set_color_images(self,color_images):
    self.__color_images = color_images

  def check_reset(self):
    events = self.__sense_hat.stick.get_events()
    if len(events) == 0:
      return 0
    else:
      return 1

  def get_row_duration(self):
    return self.__row_time

  def set_row_duration(self,new_row_duration):
    self.__row_time = new_row_duration

  def get_max_time(self):
    return self.__max_time

  def set_max_time(self):
    return self.__max_time
    
  def show_collect_message(self):
    self.__sense_hat.show_message('Sample collected')

  def missed_sample(self):
    self.__sense_hat.show_message('Missed Sample')

def test_case():
  visual_lights = LedMatrix()
  color_row = visual_lights.get_colors()['r']
  color_image = visual_lights.get_color_images()['green']
  visual_lights.change_Color(color_image)
  sleep(3)
  color_image = visual_lights.get_color_images()['yellow']
  visual_lights.change_Color(color_image)

  row_duration  = 1.875*2
  count_row = 1
  max_time = 15*2
  previous_time = time()
  current_time = 0
  
  while current_time <= max_time:
      
    if visual_lights.check_reset():
      count_row = 1
      visual_lights.show_collect_message()
      break
    current_time = time() - previous_time
    if current_time >= row_duration*count_row:
          print current_time
          print row_duration*count_row
          color_image = visual_lights.change_color_row(color_image,color_row,count_row)
          count_row += 1
      
  visual_lights.missed_sample()


if __name__ == '__test_case__':
  test_case()
