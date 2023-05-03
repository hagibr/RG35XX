from time import sleep
import struct
import termios, fcntl, sys, os
import colorsys
from fb import Framebuffer
from gfx import Rect

device = '/dev/fb0'
fb = Framebuffer(device)
white = fb.rgb(255,255,255)
black = fb.rgb(0,0,0)
fb.putstr(0, 0, "Hello RG35XX", white, 2)
sleep(1)
fb.putstr(0, 16, "This is my Python demo program for printing on screen", white, 2)
sleep(1)
for loop in range(10, 0, -1):
    fb.putstr(-1, -1, f"{loop}", white, 2)
    sleep(0.1)
    fb.putstr(-1, -1, f"{loop}", black, 2)
    fb.putstr(-1, -1, f"{loop}", white, 3)
    sleep(0.1)
    fb.putstr(-1, -1, f"{loop}", black, 3)
    fb.putstr(-1, -1, f"{loop}", white, 4)
    sleep(0.1)
    fb.putstr(-1, -1, f"{loop}", black, 4)
    fb.putstr(-1, -1, f"{loop}", white, 3)
    sleep(0.1)
    fb.putstr(-1, -1, f"{loop}", black, 3)
    fb.putstr(-1, -1, f"{loop}", white, 2)
    sleep(0.5)
    fb.putstr(-1, -1, f"{loop}", black, 2)

