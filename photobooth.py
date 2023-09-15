import pygame
import time
from threading import Thread

running = True

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_mode((800, 450))

    while running:
        handle_input()
        pygame.display.flip()
        time.sleep(0.2)

    pygame.quit()

def handle_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

Thread(target=main).start()
