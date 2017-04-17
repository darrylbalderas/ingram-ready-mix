'''
Created by: Alison Chan, Darryl Balderas, and Michael Rodriguez
Programmed in: Python 2.7
Purpose: This module was created to utilize and organize the 
functionality of the sense_hat hardware
'''
from sense_hat import SenseHat

class LedMatrix:
  def __init__(self):
    '''
    Parameters: None
    Function: Initializes an instance of LedMatrix and all of 
    the variables
    Returns: None
    '''
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
    self.__collection_time = 60*15.0
    
  def make_image(self,color):
    '''
    Parameters: color desired(string)
    Function: creates a color list from the color 
    in the parameters
    Returns: 64 color list
    '''
    image = [] 
    for i in range(self.__row*self.__column):
      image.append(self.__colors[color])
    return image
    
  def change_color(self,color_image):
    '''
    Parameters: color_image (64 color list)
    Function: changes the sense hat module matrix to the given
    color list in the parameters
    Returns: None
    '''
    self.__sense_hat.set_pixels(color_image)
    
  def change_color_row(self,color_image,new_color,row):
    '''
    Parameters: color_image( 64 color list), new_color(RBG value), row(integer)
    Function: changes the color of the row in the led matrix
    Returns: color_image
    '''
    start = (row-1) * self.__row 
    end = (row*self.__row)
    for i in range(start,end):
      color_image[i] = new_color
    self.__sense_hat.set_pixels(color_image)
    return color_image
    
  def clear_matrix(self):
    '''
    Parameters: None
    Function: clears the led matrix
    Returns: None
    '''
    self.__sense_hat.clear()

  def get_colors(self):
    '''
    Parameters: None 
    Function: Getter function for obtaining the color dictionary
    Returns: colors dictionary 
    '''
    return self.__colors

  def set_colors(self,colors):
    '''
    Parameters: colors ( color dictionary)
    Function: Setter function for changing the color dictionary
    Returns: None 
    '''
    self.__colors = colors

  def get_color_images(self):
    '''
    Parameters: None 
    Function: Getter function for obtaining the color images dictionary
    Returns: color images dictionary
    '''
    return self.__color_images
    
  def set_color_images(self,color_images):
    '''
    Parameters: color_images ( color images dictionary)
    Function: Setter function for changing the color images dictionary 
    Returns: None
    '''
    self.__color_images = color_images

  def get_row_duration(self):
    '''
    Parameters: None 
    Function: Getter function for obtaining the row duration
    Returns: row duration (integer)
    '''
    return self.__row_duration

  def set_row_duration(self,new_row_duration):
    '''
    Parameters: new_row_duration(integer)
    Function: Setter function for changing the row duration
    Returns: None
    '''
    self.__row_duration = new_row_duration

  def get_collection_time(self):
    '''
    Parameters: None
    Function: Getter function for obtaining the sample collection 
    time
    Returns: collection time
    '''
    return self.__collection_time

  def set_collection_time(self,new_collection_time):
    '''
    Parameters: new_collection_time( integer)
    Function: Setter function for changing the sample collection time
    Returns: None
    '''
    self.__collection_time = new_collection_time

  def show_message(self,message):
    '''
    Parameters: message(string)
    Function:  horizontally displays message in the led matrix
    Returns: message
    '''
    return self.__sense_hat.show_message(message,text_colour = [255,255,255])

  def ingram_colors(self,color):
    '''
    Parameters: color( string)
    Function: Make a new 64 color list
    Returns: 64 color list
    '''
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
    '''
    Parameters: None
    Function: returns green color image
    '''
    return self.__color_images['green']

  def get_redImage(self):
    '''
    Parameters: None
    Function: returns a red color image
    '''
    return self.__color_images['red']

  def get_yellowImage(self):
    '''
    Parameters: None
    Function: returns a yellow color image
    '''
    return self.__color_images['yellow']

  def get_blueImage(self):
    '''
    Parameters: None
    Function: returns a blue color image
    '''
    return self.__color_images['blue']

  def get_blue(self):
    '''
    Parameters: None 
    Function: return the RGB value for blue
    '''
    return self.__colors['b']

  def get_green(self):
    '''
    Parameters: None  
    Function: returns the RGB value for green 
    '''
    return self.__colors['g']

  def get_red(self):
    '''
    Parameters: None
    Function: returns the RGB value for red
    '''
    return self.__colors['r']

  def get_yellow(self):
    '''
    Parameters: None
    Function: returns the RGB value for yellow
    '''
    return self.__colors['y']
