import os
import pygame
import subprocess
import time
import RPi.GPIO as GPIO
from threading import Thread

IMAGE_FOLDER = "output"
BUTTON_GPIO = 27
PICTURE_TIMEOUT = 16.0

button_pressed = False
picture_time = 0.0

def main_thread():
    global button_pressed, picture_time

    if not os.path.isdir(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

    while True:
        if time.time() > picture_time + PICTURE_TIMEOUT:
            print("show idle state")

        if button_pressed:
            button_pressed = False
            take_picture()
            picture_time = time.time()

        time.sleep(0.2)

    pygame.quit()

def take_picture():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{IMAGE_FOLDER}/{timestamp}.jpg"

    succes = False
    for take in [0, 1, 2]:
        cmd("rm capt*.jpg", check=False, print_output=False)
        success = cmd("gphoto2 --capture-image-and-download", check=False).returncode == 0
        if not success: continue
        success = cmd("mv capt*.jpg {}".format(filename), check=False).returncode == 0
        if success: break
    if success:
        print_success("saved {}".format(filename))
    else:
        print_error("failed to take the image!")

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

def cmd(args, check=True, print_output=True):
    return subprocess.run(args, shell=True, check=check, capture_output=not print_output)

def print_success(message):
    print(f"\033[92m{message}\033[0m")

def print_error(message):
    print(f"\033[91m{message}\033[0m")

Thread(target=main_thread).start()
Thread(target=poll_button_thread).start()
