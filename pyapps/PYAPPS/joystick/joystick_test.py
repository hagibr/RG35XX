import struct
import time
from fb import Framebuffer
from gfx import Rect

key_map = {
    (1, 1, 0): "A_PRESSED",
    (0, 1, 0): "A_RELEASED",
    (1, 1, 1): "B_PRESSED",
    (0, 1, 1): "B_RELEASED",
    (1, 1, 2): "X_PRESSED",
    (0, 1, 2): "X_RELEASED",
    (1, 1, 3): "Y_PRESSED",
    (0, 1, 3): "Y_RELEASED",
    (1, 1, 4): "PWR_PRESSED",
    (0, 1, 4): "PWR_RELEASED",
    (1, 1, 5): "L1_PRESSED",
    (0, 1, 5): "L1_RELEASED",
    (1, 1, 6): "R1_PRESSED",
    (0, 1, 6): "R1_RELEASED",
    (1, 1, 7): "SELECT_PRESSED",
    (0, 1, 7): "SELECT_RELEASED",
    (1, 1, 8): "START_PRESSED",
    (0, 1, 8): "START_RELEASED",
    (1, 1, 9): "MENU_PRESSED",
    (0, 1, 9): "MENU_RELEASED",
    (1, 1, 10): "VOL+_PRESSED",
    (0, 1, 10): "VOL+_RELEASED",
    (1, 1, 11): "VOL-_PRESSED",
    (0, 1, 11): "VOL-_RELEASED",
    (32767, 2, 2): "L2_PRESSED",
    (-32767, 2, 2): "L2_RELEASED",
    (32767, 2, 5): "R2_PRESSED",
    (-32767, 2, 5): "R2_RELEASED",
    (-32767, 2, 6): "LEFT_PRESSED",
    (32767, 2, 6): "RIGHT_PRESSED",
    (0, 2, 6): "LEFT_RIGHT_RELEASED",
    (-32767, 2, 7): "UP_PRESSED",
    (32767, 2, 7): "DOWN_PRESSED",
    (0, 2, 7): "UP_DOWN_RELEASED",
}
js_device = "/dev/input/js0"
EVENT_SIZE = struct.calcsize("LhBB")
js_file = open(js_device, "rb")

fb_device = '/dev/fb0'
fb = Framebuffer(fb_device)
white = fb.rgb(255,255,255)
black = fb.rgb(0,0,0)

fb.putstr(-1, 0, "JOYSTICK TESTER", white, 2)
fb.putstr(-1, 16, "PRESS MENU 2x to EXIT", white, 2)


event = js_file.read(EVENT_SIZE)
last_key = " "
last_updown = " "
last_leftright = " "
last_menu_time = None
while event:
    (tv_msec,  value, type, number) = struct.unpack("LhBB", event)
    vtm = (value,type,number)
    if( vtm in key_map):
        current_key = key_map[vtm]
        
        # Each key has a position. I've decided these positions empirically.
        if( current_key == "PWR_PRESSED"):
            fb.putstr(560, 70, "PWR", white, 4)
        elif( current_key == "PWR_RELEASED"):
            fb.putstr(560, 70, "PWR", black, 4)
        elif( current_key == "VOL+_PRESSED"):
            fb.putstr(10, 70, "VOL+", white, 4)
        elif( current_key == "VOL+_RELEASED"):
            fb.putstr(10, 70, "VOL+", black, 4)
        elif( current_key == "VOL-_PRESSED"):
            fb.putstr(10, 150, "VOL-", white, 4)
        elif( current_key == "VOL-_RELEASED"):
            fb.putstr(10, 150, "VOL-", black, 4)
        elif( current_key == "L1_PRESSED"):
            fb.putstr(30, 220, "L1", white, 4)
        elif( current_key == "L1_RELEASED"):
            fb.putstr(30, 220, "L1", black, 4)
        elif( current_key == "L2_PRESSED"):
            fb.putstr(150, 220, "L2", white, 4)
        elif( current_key == "L2_RELEASED"):
            fb.putstr(150, 220, "L2", black, 4)
        elif( current_key == "R2_PRESSED"):
            fb.putstr(440, 220, "R2", white, 4)
        elif( current_key == "R2_RELEASED"):
            fb.putstr(440, 220, "R2", black, 4)
        elif( current_key == "R1_PRESSED"):
            fb.putstr(560, 220, "R1", white, 4)
        elif( current_key == "R1_RELEASED"):
            fb.putstr(560, 220, "R1", black, 4)
        elif( current_key == "LEFT_PRESSED"):
            fb.putstr(20, 350, "L", white, 4)
            fb.putstr(170, 350, "R", black, 4)
        elif( current_key == "RIGHT_PRESSED"):
            fb.putstr(170, 350, "R", white, 4)
            fb.putstr(20, 350, "L", black, 4)
        elif( current_key == "LEFT_RIGHT_RELEASED"):
            fb.putstr(20, 350, "L", black, 4)
            fb.putstr(170, 350, "R", black, 4)
        elif( current_key == "UP_PRESSED"):
            fb.putstr(95, 275, "U", white, 4)
            fb.putstr(95, 425, "D", black, 4)
        elif( current_key == "DOWN_PRESSED"):
            fb.putstr(95, 425, "D", white, 4)
            fb.putstr(95, 275, "U", black, 4)
        elif( current_key == "UP_DOWN_RELEASED"):
            fb.putstr(95, 275, "U", black, 4)
            fb.putstr(95, 425, "D", black, 4)
        elif( current_key == "MENU_PRESSED"):
            fb.putstr(-1, 300, "MENU", white, 4)
        elif( current_key == "MENU_RELEASED"):
            fb.putstr(-1, 300, "MENU", black, 4)
        elif( current_key == "X_PRESSED"):
            fb.putstr(520, 275, "X", white, 4)
        elif( current_key == "X_RELEASED"):
            fb.putstr(520, 275, "X", black, 4)
        elif( current_key == "B_PRESSED"):
            fb.putstr(520, 425, "B", white, 4)
        elif( current_key == "B_RELEASED"):
            fb.putstr(520, 425, "B", black, 4)
        elif( current_key == "Y_PRESSED"):
            fb.putstr(445, 350, "Y", white, 4)
        elif( current_key == "Y_RELEASED"):
            fb.putstr(445, 350, "Y", black, 4)
        elif( current_key == "A_PRESSED"):
            fb.putstr(595, 350, "A", white, 4)
        elif( current_key == "A_RELEASED"):
            fb.putstr(595, 350, "A", black, 4)
        elif( current_key == "SELECT_PRESSED"):
            fb.putstr(170, 450, "SELECT", white, 4)
        elif( current_key == "SELECT_RELEASED"):
            fb.putstr(170, 450, "SELECT", black, 4)
        elif( current_key == "START_PRESSED"):
            fb.putstr(340, 450, "START", white, 4)
        elif( current_key == "START_RELEASED"):
            fb.putstr(340, 450, "START", black, 4)

        # Exits on 2 quick presses on menu button
        if( current_key == "MENU_RELEASED" ):
            if( last_menu_time is not None ):
                if( time.time() - last_menu_time < 1 ):
                    break
            last_menu_time = time.time()
        elif current_key != "MENU_PRESSED":
            last_menu_time = None

        last_key = current_key

    event = js_file.read(EVENT_SIZE)