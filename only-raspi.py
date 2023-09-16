import os
import pygame
import time
import RPi.GPIO as GPIO
from threading import Thread

IMAGE_FOLDER = "output"
BUTTON_GPIO = 27

button_pressed = False

def main_thread():
    global button_pressed

    if not os.path.isdir(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    while True:
        print("show idle state")
        while not button_pressed: time.sleep(0.2)
        button_pressed = False
        print("take a picture!")
        time.sleep(16)

def poll_button_thread():
    global button_pressed

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    BUTTON_PRESS = 0
    REQUIRED_SEQUENCE = 5
    current_sequence = 0
    while True:
        if GPIO.input(BUTTON_GPIO) == BUTTON_PRESS:
            current_sequence += 1
        else:
            current_sequence = 0

        if current_sequence >= REQUIRED_SEQUENCE:
            print("button was pressed")
            button_pressed = True
            time.sleep(5)
            print("button timeout is over")

        time.sleep(0.01)

Thread(target=main_thread).start()
Thread(target=poll_button_thread).start()
