import board
import neopixel
import time
import numpy as np
pixels = neopixel.NeoPixel(board.D18, 300, auto_write=False)


def switch_colors():
    for x in range(0, 300):
        if x % 3 == 0:
            pixels[x] = (255,0,0)
        elif x % 2 == 0:
            pixels[x] = (0,255,0)
        else:
            pixels[x] = (0,0,255)
    pixels.show()
    time.sleep(2)


def rgb_color_show():
    for x in range(0, 300):
        pixels[x] = (0,255,255)
    pixels.show()
    time.sleep(2)
    for x in range(0, 300):
        pixels[x] = (255,255,0)
    pixels.show()
    time.sleep(2)
    for x in range(0, 300):
        pixels[x] = (255,0,255)
    pixels.show()
    time.sleep(2)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b)

def rainbow_cycle(wait, num_pixels):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def subtract_color(color, value):
    ret = np.subtract(color,value)
    if ret[0] < 0:
        ret[0] = 0
    elif ret[0] > 255:
        ret[0] = 255
    if ret[1] < 0:
        ret[1] = 0
    elif ret[1] > 255:
        ret[1] = 255
    if ret[2] < 0:
        ret[2] = 0
    elif ret[2] > 255:
        ret[2] = 255
    return tuple(ret)

def flow_cycle(wait, color, length, dim_value, num_pixels):
    for i in range(num_pixels):
        pixels.fill((0,0,0))
        pixels[i] = color
        if i >= 1:
            trail_val = length
            if i < length:
                trail_val = i
            for j in range(1, trail_val):
                value = subtract_color(color, tuple(d * j for d in dim_value))
                #print(str(i-j) + ': ' + str(value))
                pixels[i - j] = value
        pixels.show()
        time.sleep(wait)

def set_pixels(color, indices, wait):
    for i in indices:
        pixels[i] = color
    pixels.show()
    time.sleep(wait)

def pulse_dim(color, indices, on_time, dim_time, num_pulses, off_time):
    set_pixels(color, indices, on_time)
    interval = dim_time / num_pulses
    sub_val = (np.array(color) / num_pulses).astype(np.int32)
    prev_color = color
    for j in range(num_pulses):
        prev_color = subtract_color(prev_color, sub_val)
        #print(str(j) + ': ' + str(prev_color))
        set_pixels(prev_color, indices, interval)
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(off_time)
    
while True:
    switch_colors()
    rgb_color_show()
    flow_cycle(0.00001, (0,255,255), 50, (0,8,10), 300)
    flow_cycle(0.00001, (255,0,255), 50, (10,0,8), 300)
    flow_cycle(0.00001, (255,255,0), 50, (8,10,0), 300)
    flow_cycle(0.0001, (240,125,0), 50, (8,10,0), 300)
    flow_cycle(0.0001, (125,240,50), 50, (8,10,3), 300)
    flow_cycle(0.0001, (125,40,250), 50, (5,3,10), 300)
    flow_cycle(0.0001, (25,40,250), 50, (3,2,10), 300)
    rainbow_cycle(0.001, 300)
    rainbow_cycle(0.005, 300)
    rainbow_cycle(0.01, 300)
    pulse_dim((220,0,140), range(300), 1, 3.0, 50, 0.2)
    pulse_dim((140,210,50), range(300), 1, 3.0, 50, 0.2)
    pulse_dim((0,220,240), range(300), 2, 10.0, 100, 0.5)

