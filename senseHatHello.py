from sense_hat import SenseHat
from time import sleep

##These are the different type of colors 
def make_Color_Image(color):
    image = [] 
    for i in range(row*column):
        image.append(color)
    return image
r = [ 255,0,0 ] 

y = [ 255, 135, 0]   
 
b = [ 0,0,255]   

g = [ 0, 255, 0]   

v = [ 159, 0 , 255]   

white = [ 0, 0 , 0 ]   

row = 8
column = 8

column_minute = 0
total_minute = 10 * 8

red = make_Color_Image(r)
yellow = make_Color_Image(y)
green = make_Color_Image(g)
violet = make_Color_Image(v)
blue = make_Color_Image(b)
green = make_Color_Image(g)

sense = SenseHat()
sense.set_pixels(green)
sleep(2)
sense.set_pixels(yellow)
n = 0
multiple = 8

while column_minute != total_minute:
    sleep(10)
    n += 1
    start = (n-1)*multiple
    end = (n*multiple)
    for i in range(start,end):
        yellow[i] = r
    sense.set_pixels(yellow)
    column_minute += 10
    






