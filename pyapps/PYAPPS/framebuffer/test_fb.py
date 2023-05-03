#!/usr/bin/env python
"""Framebuffer test program

Usage: python test_fb.py [options]

Options:
  -d ..., --device=...   Framebuffer device to test, default: /dev/fb0
  -h, --help              show this help
"""

import sys
import getopt
from time import sleep
import struct
import termios, fcntl, sys, os
import colorsys
from fb import Framebuffer
from gfx import Rect


def msg(fb, s, c, max_size):
	width = fb.str_width(s)
	for i in range(max_size+1, 0, -1):
		if fb.xres > i*width:
			fb.putstr(-1, -1, s, c, i)
			return True
	return False


def show_name(fb, c):
	fb.fill(0)
	if not msg(fb, fb.name, c, 3):
		msg(fb, 'Test', c, 3)
	sleep(2)


def show_done(fb, c):
	fb.fill(0)
	msg(fb, 'Done', c, 3)
	sleep(2)


def test_blank(fb, c):
	print("  Blanking")
	fb.fill(0)
	msg(fb, 'Blank  ', c, 2)
	sleep(1)
	fb.blank(1)
	sleep(2)
	fb.fill(0)
	msg(fb, 'Unblank', c, 2)
	sleep(0.5)
	fb.blank(0)
	sleep(1)


def test_border(fb, c):
	print("  Border")
	fb.fill(0)
	fb.draw.rect(c, Rect(0, 0, fb.xres-1, fb.yres-1), 1)

	fb.draw.rect(c, Rect(2, 2, 4, 4), 0)
	fb.draw.rect(c, Rect(2, fb.yres-6, 4, 4), 0)

	fb.draw.rect(c, Rect(fb.xres-6, 2, 4, 4), 0)
	fb.draw.rect(c, Rect(fb.xres-6, fb.yres-6, 4, 4), 0)
	sleep(2)


def test_raster(fb, c):
	print("  Raster")
	fb.fill(0)
	for y in range(0, fb.yres, 2):
		for x in range(0, fb.xres, 2):
			fb.putpixel(x, y, c)
			fb.putpixel(x+1, y+1, c)
	sleep(2)


def test_rgb(fb):
	if (fb.bits_per_pixel == 1):
		return
	print("  RGB")
	fb.fill(0)
	width = (fb.xres-1)/3
	fb.draw.rect(fb.rgb(255,0,0), Rect(0, 0, width, fb.yres), 0)
	fb.putstr(5, fb.yres/2, 'RED', 0, 1)

	fb.draw.rect(fb.rgb(0,255,0), Rect(width, 0, width, fb.yres), 0)
	fb.putstr(5+width, fb.yres/2, 'GREEN', 0, 1)

	fb.draw.rect(fb.rgb(0,0,255), Rect(2*width, 0, width, fb.yres), 0)
	fb.putstr(5+2*width, fb.yres/2, 'BLUE', 0, 1)
	sleep(2)


def test_colors(fb):
	if (fb.bits_per_pixel != 16):
		return
	print("  Colors")

	fb.fill(0)
	fb.fbp.seek(0)
	step = fb.xres * fb.yres
	for i in range(0, step):
			h = i/float(step)
			rgb = colorsys.hsv_to_rgb(h, 1, 1)
			red = int(rgb[0] * ((1 << fb.red.length) - 1))
			green = int(rgb[1] * ((1 << fb.green.length) - 1))
			blue = int(rgb[2] * ((1 << fb.blue.length) - 1))
			color = fb.rgb(red, green, blue)
			fb.fbp.write(struct.pack("H", color))
	sleep(2)


def usage():
	print(__doc__)

def main(argv):
	device = '/dev/fb0'
	try:
		opts, args = getopt.getopt(argv, "hd:", ["help", "device="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-d", "--device"):
			device = arg

	fb = Framebuffer(device)
	print(fb)

	red = fb.rgb(255,0,0)
	yellow = fb.rgb(255,255,0)
	green = fb.rgb(0,255,0)

	show_name(fb, red)

	print("Tests:")

	test_border(fb, yellow)

	test_rgb(fb)

	test_colors(fb)

	test_raster(fb, red)

	test_blank(fb, red)

	show_done(fb, red)

	fb.fill(0)
	fb.close()

if __name__ == '__main__':
	main(sys.argv[1:])
