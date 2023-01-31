import math
import utime
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

# define buffer handling elements
buffer = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()
displaywidth = GalacticUnicorn.WIDTH

# define colours and font
fg = buffer.create_pen(255,20,147)
bg = buffer.create_pen(0,0,0)
buffer.set_font("bitmap8")

def cycle(type):
    
    #set initial variables
    killswitch = True
    message = "Go get 'em"
    tally = 0
    
    while killswitch:
        buffer.set_pen(fg)
        width = buffer.measure_text(message, 1)
        display_size = GalacticUnicorn.WIDTH
        start_position = int((display_size - width) / 2) + 1
        buffer.text(message, start_position, 2, -1, 1)
        gu.update(buffer)
        utime.sleep(1)
            
        fill(type)
        
        killswitch = empty(type, tally)
        
        if type == "work":
            tally = tally + 1
            type = "rest"
            message = "Break time!"
        else:
            type = "work"
            message = "Go get 'em"
        
def fill(type):
    red = 255
    green = 255
    blue = 255
    
    #erase status message
    for a in range(53):
        for b in range(11):
            buffer.set_pen(bg)
            buffer.pixel(a, b)
            gu.update(buffer)
            utime.sleep(0.0001)
    
    #fill with red to yellow or blue to green rainbow
    for x in range(53):
        if type == "work":
            green = int(4.81 * x)
        else:
            red = int(4.81 * x)
        for y in range(11):
            blue = int(4.81 * y)
            dotpen = buffer.create_pen(red, green, blue)
            buffer.set_pen(dotpen)
            buffer.pixel(x, y)
            gu.update(buffer)
            utime.sleep(0.0001)

def empty(type, tally):
    #set variables
    row = 10
    column = 52
    buffer.set_pen(bg)
    
    #calculate rest between each LED extinguishing
    if type == "work":
        delay = 2572
    else:
        delay = 515
 
    if ((tally & 3) == 0) and type == "rest":
        delay = 2058
    
    #blink out one pixel at a time
    while row > -1:
        while column > -1:
            buffer.pixel(column, row)
            gu.update(buffer)
            column = column - 1
            for zzz in range(delay):
                if gu.is_pressed(GalacticUnicorn.SWITCH_C):
                    buffer.set_pen(bg)
                    buffer.clear()
                    gu.update(buffer)
                    killswitch = True
                    return killswitch
                elif gu.is_pressed(GalacticUnicorn.SWITCH_D):
                    buffer.set_pen(bg)
                    buffer.clear()
                    gu.update(buffer)
                    #set termination flag
                    killswitch = False
                    return killswitch
                else:
                    utime.sleep(0.001)
        column = 52
        row = row - 1
    killswitch = True
    return killswitch

while True:
    while gu.is_pressed(GalacticUnicorn.SWITCH_A):
        buffer.set_pen(bg)
        buffer.clear()
        gu.update(buffer)
        cycle("work")
