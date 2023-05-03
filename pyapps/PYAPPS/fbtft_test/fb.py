import os, sys
import fcntl, mmap, struct

import gfx

# definitions from linux/fb.h
FBIOGET_VSCREENINFO = 0x4600
FBIOGET_FSCREENINFO = 0x4602
FBIOBLANK = 0x4611

FB_TYPE_PACKED_PIXELS= 0
FB_TYPE_PLANES = 1
FB_TYPE_INTERLEAVED_PLANES = 2
FB_TYPE_TEXT = 3
FB_TYPE_VGA_PLANES = 4
FB_TYPE_FOURCC = 5

FB_VISUAL_MONO01 = 0
FB_VISUAL_MONO10 = 1
FB_VISUAL_TRUECOLOR = 2
FB_VISUAL_PSEUDOCOLOR = 3
FB_VISUAL_DIRECTCOLOR = 4
FB_VISUAL_STATIC_PSEUDOCOLOR = 5
FB_VISUAL_FOURCC = 6

FB_BLANK_UNBLANK = 0
FB_BLANK_POWERDOWN = 4



# Kind of like a pygame Surface object, or not!
# http://www.pygame.org/docs/ref/surface.html
class Framebuffer(gfx.BaseGFX):
	
	def __init__(self, dev):
		self.dev = dev
		self.fbfd = os.open(dev, os.O_RDWR)
		vinfo = struct.unpack("8I12I16I4I", fcntl.ioctl(self.fbfd, FBIOGET_VSCREENINFO, " "*struct.calcsize("8I12I16I4I")))
		finfo = struct.unpack("16cL4I3HI", fcntl.ioctl(self.fbfd, FBIOGET_FSCREENINFO, " "*struct.calcsize("16cL4I3HI")))

		bytes_per_pixel = (vinfo[6] + 7) // 8 # bits_per_pixel {1,16,32} -> bytes_per_pixel {1,2,4}
		screensize = vinfo[17] # smem_len

		fbp = mmap.mmap(self.fbfd, screensize, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ|mmap.PROT_WRITE)

		self.fbp = fbp
		self.xres = vinfo[0]
		self.yres = vinfo[1]
		self.xoffset = vinfo[4]
		self.yoffset = vinfo[5]
		self.bits_per_pixel = vinfo[6]
		self.bytes_per_pixel = bytes_per_pixel
		self.grayscale = vinfo[7]
		self.red = gfx.Bitfield(vinfo[8], vinfo[9], vinfo[10])
		self.green = gfx.Bitfield(vinfo[11], vinfo[12], vinfo[13])
		self.blue = gfx.Bitfield(vinfo[14], vinfo[15], vinfo[16])
		self.transp = gfx.Bitfield(vinfo[17], vinfo[18], vinfo[19])
		self.nonstd = vinfo[20]
		self.name = ''.join([chr(ord(x)) for x in finfo[0:15] if x != b'\x00'])
		self.type = finfo[18]
		self.visual = finfo[20]
		self.line_length = finfo[24]
		self.screensize = screensize

		self.draw= gfx.Draw(self)

	def close(self):
		self.fbp.close()
		os.close(self.fbfd)

	def blank(self, blank):
		# Blanking is not supported by all drivers
		try:
			if blank:
				fcntl.ioctl(self.fbfd, FBIOBLANK, FB_BLANK_POWERDOWN)
			else:
				fcntl.ioctl(self.fbfd, FBIOBLANK, FB_BLANK_UNBLANK)
		except IOError:
			pass

	def __str__(self):
		visual_list = ['MONO01', 'MONO10', 'TRUECOLOR', 'PSEUDOCOLOR', 'DIRECTCOLOR', 'STATIC PSEUDOCOLOR', 'FOURCC']
		type_list = ['PACKED_PIXELS', 'PLANES', 'INTERLEAVED_PLANES', 'TEXT', 'VGA_PLANES', 'FOURCC']
		visual_name = 'unknown'
		if self.visual < len(visual_list):
			visual_name = visual_list[self.visual] 
		type_name = 'unknown'
		if self.type < len(type_list):
			type_name = type_list[self.type]

#		"    geometry 176 220 176 220 16\n"

		return \
		"mode \"%sx%s\"\n" % (self.xres, self.yres) + \
		"    nonstd %s\n" % self.nonstd + \
		"    rgba %s/%s,%s/%s,%s/%s,%s/%s\n" % (self.red.length, self.red.offset, self.green.length, self.green.offset, self.blue.length, self.blue.offset, self.transp.length, self.transp.offset) + \
		"endmode\n" + \
		"\n" + \
		"Frame buffer device information:\n" + \
		"    Device      : %s\n" % self.dev + \
		"    Name        : %s\n" % self.name + \
		"    Size        : %s\n" % self.screensize + \
		"    Type        : %s\n" % type_name + \
		"    Visual      : %s\n" % visual_name + \
		"    LineLength  : %s\n" % self.line_length


