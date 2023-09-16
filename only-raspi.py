import os
import pygame
import subprocess
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
        take_picture()
        time.sleep(16)

def take_picture():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "{}/{}.jpg".format(IMAGE_FOLDER, timestamp)

    succes = False
    for take in [0, 1, 2]:
        cmd("rm capt*.jpg", check=False, print_output=False)
        success = cmd("gphoto2 --capture-image-and-download", check=False).returncode == 0
        if not success: continue
        success = cmd("mv capt*.jpg {}".format(filename), check=False).returncode == 0
        if success: break
    if success:
        print("saved {}".format(filename))
    else:
        print("failed to take the image!")

def cmd(args, check=True, print_output=True):
    return subprocess.run(args, shell=True, check=check, capture_output=not print_output)

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
