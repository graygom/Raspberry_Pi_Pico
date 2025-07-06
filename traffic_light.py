#
# TITLE:
# AUTHOR: Hyunseung Yoo
# PURPOSE:
# REVISION:
# REFERENCE: Get started with MicroPython on Raspberry Pi Pico, 1st ed. (2021), Raspberry Pi Press
#

import machine
import utime
import _thread

# GPIO setting
led_r  = machine.Pin(12, machine.Pin.OUT) 								# GP12, out
led_g  = machine.Pin(13, machine.Pin.OUT) 								# GP13, out
led_b  = machine.Pin(14, machine.Pin.OUT) 								# GP14, out
buzzer = machine.Pin(16, machine.Pin.OUT) 								# GP16, out

# check button thread
global button_pressed
button_pressed = False

def button_reader_thread():
    global button_pressed
    # GPIO setting
    button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)			# GP15, in
    # check button
    while True:
        if button.value() == 1:
            button_pressed = True

# start check button thread
_thread.start_new_thread(button_reader_thread, ())

# main thread
while True:
    #
    led_r.value(1)
    led_g.value(0)
    led_b.value(0)
    buzzer.value(0)
    
    # check button
    if button_pressed == 1:
        print('button pressed!')
        led_r.value(0)
        led_g.value(1)
        led_b.value(0)
        for i in range(10):
            buzzer.value(1)    
            utime.sleep(0.02)
            buzzer.value(0)
            utime.sleep(0.02)
        
        print('back to Red sign.')
        led_r.value(1)
        led_g.value(0)
        led_b.value(0)
        button_pressed = 0
