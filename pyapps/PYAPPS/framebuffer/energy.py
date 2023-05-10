from time import sleep
import struct
import termios, fcntl, sys, os
import colorsys
from fb import Framebuffer
from gfx import Rect

fb = Framebuffer('/dev/fb0')
white = fb.rgb(255,255,255)
black = fb.rgb(0,0,0)

# Opening joystick device and configuring it as non-blocking
joystick = open("/dev/input/js0", "rb")
os.set_blocking(joystick.fileno(), False)
EVENT_SIZE = struct.calcsize("LhBB")

while(True):
    # Process all joystick pending events
    while(joystick.peek(EVENT_SIZE)):
        event = joystick.read(EVENT_SIZE)
        (tv_msec, value, type, number) = struct.unpack("LhBB", event)
        vtm = (value,type,number)
        # Power button released?
        if( vtm == (0, 1, 4) ):
            exit()
        # print(vtm)

    fb.fill(black)
    cline = 0
    
    fb.putstr(-1,cline*16,"/sys/class/power_supply/", white, 2)
    cline += 1

    with open("/sys/class/power_supply/atc260x-usb/uevent", "rt") as usb_file:
        fb.putstr(-1, cline*16, "atc260x-usb", white, 2)
        cline += 1
        usb_lines = usb_file.readlines()
        for line in usb_lines:
            fb.putstr(0, cline*16, line.replace("\n", ""), white, 2)
            cline += 1

    with open("/sys/class/power_supply/atc260x-wall/uevent", "rt") as wall_file:
        fb.putstr(-1, cline*16, "atc260x-wall", white, 2)
        cline += 1
        wall_lines = wall_file.readlines()
        for line in wall_lines:
            fb.putstr(0, cline*16, line.replace("\n", ""), white, 2)
            cline += 1

    with open("/sys/class/power_supply/battery/uevent", "rt") as battery_file:
        fb.putstr(-1, cline*16, "battery", white, 2)
        cline += 1
        battery_lines = battery_file.readlines()
        for line in battery_lines:
            fb.putstr(0, cline*16, line.replace("\n", ""), white, 2)
            cline += 1
    sleep(1)

    

print(usb_lines)
print(wall_lines)
print(battery_lines)



