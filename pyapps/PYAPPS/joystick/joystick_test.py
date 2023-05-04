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
    (-32767, 2, 7): "UP_PRESSED",
    (32767, 2, 7): "DOWN_PRESSED",
    (0, 2, 7): "UP_DOWN_RELEASED",
    (-32767, 2, 6): "LEFT_PRESSED",
    (32767, 2, 6): "RIGHT_PRESSED",
    (0, 2, 6): "LEFT_RIGHT_RELEASED",
    (32767, 2, 2): "L2_PRESSED",
    (-32767, 2, 2): "L2_RELEASED",
    (32767, 2, 5): "R2_PRESSED",
    (-32767, 2, 5): "R2_RELEASED",
}
js_device = "/dev/input/js0"
EVENT_SIZE = struct.calcsize("LhBB")
js_file = open(js_device, "rb")

device = '/dev/fb0'
fb = Framebuffer(device)
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
        
        # Correcting the UP_DOWN_RELEASED to UP_RELEASED or DOWN_RELEASED
        if( current_key == "UP_DOWN_RELEASED" ):
            if( last_updown == "UP_PRESSED" ):
                current_key = "UP_RELEASED"
            elif( last_updown == "DOWN_PRESSED" ):
                current_key = "DOWN_RELEASED"
        # Same with LEFT_RIGHT_RELEASED
        elif( current_key == "LEFT_RIGHT_RELEASED" ):
            if( last_leftright == "LEFT_PRESSED" ):
                current_key = "LEFT_RELEASED"
            elif( last_leftright == "RIGHT_PRESSED" ):
                current_key = "RIGHT_RELEASED"
        
        fb.putstr(-1, -1, last_key, black, 4)
        fb.putstr(-1, -1, current_key, white, 4)

        # Exits on 2 quick presses on menu button
        if( current_key == "MENU_RELEASED" ):
            if( last_menu_time is not None ):
                if( time.time() - last_menu_time < 1 ):
                    break
            last_menu_time = time.time()
        elif current_key != "MENU_PRESSED":
            last_menu_time = None

        last_key = current_key

        # UP_DOWN_RELEASED / LEFT_RIGHT_RELEASED logic
        if( last_key == "UP_PRESSED" ):
            last_updown = "UP_PRESSED"
        elif( last_key == "DOWN_PRESSED" ):
            last_updown = "DOWN_PRESSED"
        elif( last_key == "LEFT_PRESSED" ):
            last_leftright = "LEFT_PRESSED"
        elif( last_key == "RIGHT_PRESSED" ):
            last_leftright = "RIGHT_PRESSED"
        
    event = js_file.read(EVENT_SIZE)