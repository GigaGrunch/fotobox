import pygame
import time
from threading import Thread

running = True
photo_timestamp = 0
photo_timeout = 16
state = 0
screen = None

def main():
    global screen, state

    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((1920, 1080))

    while running:
        handle_input()

        if state != STATE_IDLE:
            print("enter idle state")
            texture = pygame.Surface(screen.get_size()).convert()
            texture.fill(pygame.Color("black"))
            font = pygame.font.Font(None, 500)
            text = font.render("IDLE", 1, (227, 157, 200))
            text_rect = text.get_rect()
            texture_rect = texture.get_rect()
            text_rect.centerx = texture_rect.centerx
            text_rect.centery = texture_rect.centery
            texture.blit(text, text_rect)
            screen.blit(texture, (0, 0))
            pygame.display.flip()
            state = STATE_IDLE

        time.sleep(0.2)

    pygame.quit()

def handle_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

Thread(target=main).start()

STATE_IDLE = 10
STATE_SHOWING_PHOTO = 20
