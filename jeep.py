import pygame
from gpiozero import *
from time import sleep
from threading import Timer

# Initialise gpio
button = Button(3)
ballSensor = Button(21, pull_up = True)
hs = OutputDevice(2)
smoke = OutputDevice(14)

# FUNCTIONS

def relay_handshake():
    hs.off()
    print "Handshake"    
    hs.on()
    sleep(0.05)
    hs.off()
    sleep(0.05)
    hs.on()
    sleep(0.05)
    hs.off()
    sleep(0.05)
    hs.on()
    sleep(0.05)
    hs.off()
    sleep(0.05)
    hs.on()
    sleep(0.05)
    hs.off()

# Raise vol over time
def vol_ramp(sound):
    sound.set_volume(0)
    volume = 0.0
    while sound.get_volume() != 1:
        print sound.get_volume()
        volume = volume + 0.1
        sound.set_volume(volume)
        sleep(0.1)
    
# Ball detect 
def ball_trigger():
    print("Ball")

    #Pause background music
    bg.pause()

    #Play sound effect
    fx.play(effect)
    
    #Fire smoke machine
    smoke.on()
    
    #Wait for 2 seconds
    sleep(2)

    #Stop Smoke Machine
    smoke.off()
    
    sleep(effect.get_length() - 2)
    #Unpause background music
    bg.unpause()
    vol_ramp(background)
    print("Reset")

def status_quo():
    while bg.get_busy() == True:
        button.when_pressed = ball_trigger
        continue

# Initialise the audio mixer
print "Initialise mixer"
pygame.init()
while pygame.mixer.get_init() == False:
    continue

#Get Channels
bg = pygame.mixer.Channel(0)
fx = pygame.mixer.Channel(1)

# Load sounds
print "Load sounds"
background = pygame.mixer.Sound("bg.ogg")
effect = pygame.mixer.Sound("jeepstart.ogg")

#Turn on relays after delay
t = Timer(1 * 60, relay_handshake)
t.start()
#relay_handshake()

# Play background sound forever
print "Loop background music"
bg.play(background, loops=-1)
#print background.get_length()
   
while True == True:
    status_quo();
