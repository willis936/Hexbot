"""

Hexabot v1.0
2013/07/03
Paul Willis
 
All coordinates assume a screen resolution of 1366x768, and
windowed mode at the default location.  Steam, W7 XP theme.

Developed in:
    IDLE, Python 2.7.5, 32 bit
    Windows 7 Home Premium SP1, 64 bit

Libraries:
    Python Image Tools 1.1.7 for Python 2.7, 32 bit
    Pywin32 Build 218 for Python 2.7, 32 bit
    NumPy 1.7.1, 32 bit

"""

import Image
import ImageFilter
import ImageGrab
import ImageOps
import math
from numpy import *
import os
import random
import time
import win32api
import win32con


# Globals
# ------------------
 
x_pad = 299
y_pad = 144
x_size = 768
y_size = 480
xy_ratio = x_size / y_size

n_rays = 60

# ------------------


def main():

    assemble()
    
    # im = screen_grab()
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')


# Returns screen area of game
def screen_grab():
    
    box = (x_pad, y_pad, x_pad + x_size, y_pad + y_size)
    im = ImageGrab.grab(box)
    
    #im = ImageOps.equalize(im)
    #im = im.filter(ImageFilter.FIND_EDGES)
    
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')
    
    return im


# Find the hexagon, triangle, and blocks.
def assemble():
    
    im = screen_grab()
    
    # Create and traverse rays from center, saving triangle location.
    # i is the ray counter.
    for i in range(0, n_rays):
        
        trig_entry = (2 * i * math.pi) / n_rays

        x_start = x_size / 2
        y_start = y_size / 2 
        
        x_last = int(round(x_start + ((cos(trig_entry) * x_size / 20))))
        y_last = int(round(y_start + ((sin(trig_entry) * xy_ratio * y_size / 20))))
        
        x = int(round(x_start + ((cos(trig_entry) * x_size / 5))))
        y = int(round(y_start + ((sin(trig_entry) * xy_ratio * y_size / 5))))

        print '{}:\t({}, {}) --> ({}, {}) {}'.format(i, x_last, y_last, \
                                                      x, y, trig_entry)

        triangle = 0
        
        edge_count = 0
        edge_size = x_size
        edge_size_last = 0

        line = get_line(x_last, y_last, x, y)
        line_length = len(line)
        
        # ray debug
        ray_R = int(round(random.random() * 255))
        ray_G = int(round(random.random() * 255))
        ray_B = int(round(random.random() * 255))
        
        # Only search small region of screen.  j is the pixel counter.
        for j in range (1, line_length):
            
            R_last, G_last, B_last = im.getpixel(line[j - 1])
            
            R, G, B = im.getpixel(line[j])
            
            if j > 1: #debug rays
                im.putpixel(line[j - 2], (ray_R, ray_G, ray_B))

            if R_last != R and G_last != G and B_last != B:
                edge_size = edge_size_last
                if edge_size < (x_size / 275) and edge_size > 0:
                    im.save(os.getcwd() + '\\Snap__' + #debug triangle
                            str(int(time.time())) + '.png')
                    triangle = line[j]
                    print 'The triangle is at {0}.'.format(triangle)
                    break
                edge_count += 1
                edge_size_last = 0
            else:
                edge_size_last += 1
        if triangle != 0:
            break
    im.save(os.getcwd() + '\\Snap__' + #debug rays
                            str(int(time.time())) + '.png')
    '''
    # Create and traverse rays from triangle, saving edge locations.
    # i is the ray counter.
    for i in range(0, n_rays - 1):
        
        x_last = triangle.x
        y_last = triangle.y

        # Traverse ray to find the edge.  j is the pixel counter.
        for j in range (int((x_size / 2)), int(x_size / 5)):
            break'''


# Bresenham's algorithm for traversing lines.
# http://roguebasin.roguelikedevelopment.org/
#   index.php?title=Bresenham's_Line_Algorithm#Python
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


# Holds down left click
def left_down():
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    
    #time.sleep(.05)
    #print 'left Down'


# Releases left click
def leftUp():
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
    #time.sleep(.05)
    #print 'left release'



if __name__ == '__main__':
    main()



'''

# This is unfinished, untested, or unneeded code.

# Clicks into hexagon
def startGame():
    
    time.sleep(2)
    
    left_own()
    time.sleep(.1)
    left_up()
    
    left_down()
    time.sleep(.1)
    left_up()


# Updates game state
def update_data():
    im = screen_grab()
    # Crops central 1/3 of x axis and 1/2 of y axis.
    center = (x_size / 3, y_size / 4, x_size * (2/3), y_size * (3/4))
    im = im.crop(center)
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')


# Holds down right click
def right_down():
    
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

    #time.sleep(.05)
    #print 'right Down'


# Releases right click         
def right_up():
    
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    
    #time.sleep(.05)
    #print 'right release'

'''
