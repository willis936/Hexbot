"""
--------------------------------------------------------------------------------

Hexabot v1.0.02
2014/05/05
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

Notes:
    Before trying to read this code play Super Hexagon for a while.
    You need a decent understanding of the objective and how to play.
    
    The overall shape is not always a hexagon.  In the first level it
    changes to a pentagon and square so assumptions based on the shape
    are thrown out without first identifying the shape which is inefficient.
    
    The size of the inner hexagon also varies as does the "angle" of the
    entire screen so the shape is irregular.  This throws out many more
    simplifications in reconstructing the field.

Glossary:
    hexagon - innermost shape
    triangle - player
    edge - any change in color on the screen
    block - any edge that, if the triangle touches, causes the game to end
    

--------------------------------------------------------------------------------
"""

# Libraries
# ------------------
import Image
import ImageFilter
import ImageGrab
import ImageOps
import math
from numpy import *
import os
import random
import sys
import time
import win32api
import win32con

# ------------------
# Globals
# ------------------


# pixel offsets from upper left origin
x_pad = 299
y_pad = 144

# window size
x_size = 768
y_size = 480

# aspect ratio
xy_ratio = float(x_size) / y_size

# how many rays to shoot out from center
n_rays = 90


# ------------------


def main():
    
    # open log file
    old_stdout = sys.stdout
    log_file = open('hexalog_' + str(int(time.time())) + '.txt','w')
    sys.stdout = log_file
    
    assemble()
    hexagon()
    
    # close log file
    sys.stdout = old_stdout
    log_file.close()
    
    # debug runtime
    #im = screen_grab()
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')


# Returns screen area of game
def screen_grab():
    
    box = (x_pad, y_pad, x_pad + x_size, y_pad + y_size)
    im = ImageGrab.grab(box)
    
    # experimental filters, lots of computation for little benefit
    #im = ImageOps.equalize(im)
    #im = im.filter(ImageFilter.FIND_EDGES)
    
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')
    
    return im


# Find the hexagon, triangle, and blocks.
def assemble():
    
    im = screen_grab()
    
    print'ray #\t\tpoints\t\t\ttrig entry'

    triangle_ping = 0
    
    # Create and traverse rays from center, saving triangle location.
    # i is the ray counter.
    for i in range(0, n_rays):
        
        # flag for finding the triangle
        triangle = 0
        
        # when changes in color are seen these values change
        edge_count = 0
        edge_size = 0
        edge_size_last = 0
        
        # center of game screen
        x_start = x_size / 2
        y_start = y_size / 2
        
        # this is "theta" for the i'th ray in radians
        trig_entry = (2 * i * math.pi) / n_rays
        
        # start ray traverse 1/35 of the way in, skip empty area
        x_last = int(round(x_start + ((cos(trig_entry) * x_size / 35))))
        y_last = int(round(y_start + ((sin(trig_entry) \
                                       * xy_ratio * y_size / 35))))
        
        # end 1/7 of the way in, enough to find triangle and blocks
        x = int(round(x_start + ((cos(trig_entry) * x_size / 7))))
        y = int(round(y_start + ((sin(trig_entry) \
                                  * xy_ratio * y_size / 7))))
        
        # debug ray info
        print '{}:\t({}, {}) --> ({}, {})\t' \
            '{}'.format(i, x_last, y_last, x, y, trig_entry)
        
        # construct the ray line
        line = get_line(x_last, y_last, x, y)
        line_length = len(line)
        
        # Only search small region of screen.  j is the pixel counter.
        for j in range (1, line_length):
            
            R_last, G_last, B_last = im.getpixel(line[j - 1])
            
            R, G, B = im.getpixel(line[j])

            #''' ray debug
            if j > 0 and n_rays < 120:
                ray_R = int(round(255 * float(i) / n_rays))
                ray_G = int(round(255 - (255 * float(i) / n_rays)))
                ray_B = int(round(128 + (255 * float(i) / n_rays)))
                if ray_B > 255:
                    ray_B = int(round(383 - (255 * (float(i) / n_rays))))
                im.putpixel(line[j - 1], (ray_R, ray_G, ray_B))
            #'''
            
            # Compare current and last pixel.
            if R_last != R and G_last != G and B_last != B:
                
                # Check edge size past hexagon.
                if edge_count > 1:

                    # FIX THIS CODE!!!
                    
                    # Ray pinging an edge, compare edge size to last ping.
                    if ((edge_size < (edge_size_last * 1.1) \
                    or edge_size > (edge_size_last * 0.9))
                    and edge_size < x_size / 15):
                        
                        triangle_ping += 1
                        print'ping {}'.format(triangle_ping)
                        #debug ping
                        im.putpixel(line[j], (255 - R, 255 - G, 255 - B))
                        break
                    
                    # This wasn't the triangle, reset the ping.
                    else:
                        print 'ping reset'
                    triangle_ping = 0
                    
                    # Check to see if the triangle base was pinged.
                    if triangle_ping >= n_rays / 60 and \
                       triangle_ping <= n_rays / 15:
                            triangle = line[j]
                            print 'The triangle is at {0}.'.format(triangle)
                            im.save(os.getcwd() + '\\Snap__' + #debug rays
                            str(int(time.time())) + '.png')
                            break
                
                # Update size of current edge and add to edge count.
                edge_size = edge_size_last
                edge_count += 1
                edge_size_last = 0
                
            else:
                edge_size_last += 1
                
        # Stop traversing rays after triangle is found.
        if triangle != 0:
            tri_loc = [x, y]
            im.save(os.getcwd() + '\\SnapF+_' +
                            str(int(time.time())) + '.png')
            #break
    
    # debug rays    
    im.save(os.getcwd() + '\\SnapF-_' +
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

def hexagon()


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


# Deduplicate a list
def uniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output



# Run the main function
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
