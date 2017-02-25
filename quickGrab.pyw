"""

Paul Willis
2013/07/01

Steam Super Hexagon, W7 XP theme.

All coordinates assume a screen resolution of 1366x768, and
windowed mode at the default location.

Developed in IDLE, Python 2.7.5 32 bit
Python Image Tools 1.1.7 for Python 2.7 32 bit
Pywin32 Build 218 for Python 2.7 32 bit
Windows 7 Home Premium SP1 64 bit

"""

import Image
import ImageFilter
import ImageGrab
import ImageOps
import os
import time

# Globals
# ------------------
 
x_pad = 299
y_pad = 144
x_size = 768
y_size = 480

# ------------------
 
def screenGrab():
    box = (x_pad, y_pad, x_pad + x_size, y_pad + y_size)
    im = ImageGrab.grab(box)
    #im = im.filter(ImageFilter.SMOOTH)
    #im = im.filter(ImageFilter.SMOOTH_MORE)
    im = ImageOps.equalize(im)
    ##im = im.filter(ImageFilter.EDGE_ENHANCE)
    ##im = ImageOps.autocontrast(im)
    ##im = ImageOps.posterize(im, 1)
    im = im.filter(ImageFilter.FIND_EDGES)
    #center = (x_size / 3, y_size / 4, x_size * 2 / 3, y_size * 3 / 4)
    #im = im.crop(center)
    #center = im.getbbox()
    #im = im.crop(center)
    im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png')

def main():
    screenGrab()

if __name__ == '__main__':
    main()
