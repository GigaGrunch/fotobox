import os
import pygame
import subprocess
import time
import RPi.GPIO as GPIO
from threading import Thread

IMAGE_FOLDER = "output"
BUTTON_GPIO = 27
PICTURE_TIMEOUT = 16.0
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FONT_SIZE = 500
FONT_COLOR = (227, 157, 200)

button_pressed = False
picture_time = 0.0

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
texture = pygame.Surface(screen.get_size()).convert()
font = pygame.font.Font(None, FONT_SIZE)

def main_thread():
    global screen, texture, font, button_pressed, picture_time

    if not os.path.isdir(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    while True:
        if time.time() > picture_time + PICTURE_TIMEOUT:
            show_idle_state()

        if button_pressed:
            button_pressed = False

            show_countdown()

            image_path = take_picture()
            if image_path == None:
                show_error_state()
            else:
                show_picture(image_path)

            picture_time = time.time()

        time.sleep(0.2)

    pygame.quit()

def show_picture(file_path):
    texture.fill((0, 0, 0))
    try:
        image = pygame.image.load(file_path)
    except:
        print_error(f"failed to load image from '{file_path}'")
        show_error_state()
        return

    screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
    image_ratio = image.get_width() / image.get_height()

    scaled_height = int(SCREEN_HEIGHT)
    scaled_width = int(scaled_height * image_ratio)
    image = pygame.transform.scale(image, (scaled_width, scaled_height))

    x_offset = int((SCREEN_WIDTH - scaled_width) / 2.0)

    texture.blit(image, (x_offset, 0))
    screen.blit(texture, (0, 0))
    pygame.display.flip()

def show_countdown():
    for text in ["Achtung!", "Achtung!", "3", "2", "1", ""]:
        texture.fill((0, 0, 0))
        blit_line(text)
        screen.blit(texture, (0, 0))
        pygame.display.flip()
        time.sleep(0.7)

def show_idle_state():
    texture.fill((0, 0, 0))

    blit_line("Knopf", -1)
    blit_line("drücken!", 1)

    screen.blit(texture, (0, 0))
    pygame.display.flip()

def show_error_state():
    texture.fill((0, 0, 0))
    blit_line("Error :(")
    screen.blit(texture, (0, 0))
    pygame.display.flip()

def blit_line(line, pos=0):
    line = font.render(line, 1, FONT_COLOR)
    line_rect = line.get_rect()
    line_rect.centerx = int(SCREEN_WIDTH / 2.0)
    line_rect.centery = int((SCREEN_HEIGHT + line_rect.height * pos) / 2.0)
    texture.blit(line, line_rect)

def take_picture():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{IMAGE_FOLDER}/{timestamp}.jpg"

    succes = False
    for take in [0, 1, 2]:
        cmd("rm capt*.jpg", check=False, print_output=False)
        success = cmd("gphoto2 --capture-image-and-download", check=False).returncode == 0
        if not success: continue
        success = cmd("mv capt*.jpg {}".format(file_path), check=False).returncode == 0
        if success: break
    if success:
        print_success("saved {}".format(file_path))
        return file_path
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
