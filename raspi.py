import requests
import time
import RPi.GPIO as GPIO
from threading import Thread

BUTTON_GPIO = 27

def poll_button_thread():
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
            for number in [1, 2, 3]:
                print("send GET request")
                response = requests.get("http://cheesepad:8000/take_picture")
                if response.status_code == 200: break
            time.sleep(5)
            print("button timeout is over")

        time.sleep(0.01)

Thread(target=poll_button_thread).start()
