#!/usr/bin/env python2.7
# script by Charlie Langridge of Penguin Media Solutions

import RPi.GPIO as GPIO
import time
import pygame
GPIO.setmode(GPIO.BCM)

# Setup the IR sensor on PIN 22 (BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup the relay output on PIN 20 (BCM)
GPIO.setup(20, GPIO.OUT)
time_stamp = time.time()
# setup fxsequence variable
fxsequence = 0

# Raise vol over time
def vol_ramp(sound):
    sound.set_volume(0)
    volume = 0.0
    while sound.get_volume() != 1:
        print (sound.get_volume())
        volume = volume + 0.1
        sound.set_volume(volume)
        time.sleep(0.1)

# now we'll define the threaded callback function
# this will run in another thread when our event is detected
def my_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 1:
        global fxsequence
        # Ball trigger run code
        if fxsequence == 0:
            
            fxsequence = 1
            print ("Ball detected")

            #Pause background music
            bg.pause()

            #Play sound effect
            fx.play(effect)

            # Trigger Smoke
            GPIO.output(20, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(20, GPIO.LOW)

            # wait until effct music is finsihed
            time.sleep(effect.get_length() - 2)
            
            
            #Unpause background music
            bg.unpause()
            vol_ramp(background)

            # Reset pause
            
            fxsequence = 0
            print (fxsequence)
        else:
            print ("FX Sequence already in progress")
    time_stamp = time_now
    
# Initialise the audio mixer
print ("Initialise mixer")
pygame.init()
while pygame.mixer.get_init() == False:
    continue
print ("Sound effects engine started\n")

#Get Channels
bg = pygame.mixer.Channel(0)
fx = pygame.mixer.Channel(1)

# Load sounds
print ("Load sounds")
background = pygame.mixer.Sound("bg.ogg")
effect = pygame.mixer.Sound("jeepstart.ogg")

# Play background sound forever
print ("Loop background music")
bg.play(background, loops=-1)

# The GPIO.add_event_detect() line below set things up so that
# when a rising edge is detected on port 24, regardless of whatever 
# else is happening in the program, the function "my_callback" will be run
# It will happen even while the program is waiting for
# a falling edge on the other button.
GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback, bouncetime=200)

try:
    while True:
        if fxsequence == 0:
            print ("Awaiting Ball")
        else:
            print("FX Sequence in progress")
        time.sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit
