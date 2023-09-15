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

        if state != STATE_IDLE: enter_idle_state()

        time.sleep(0.2)

    pygame.quit()

def handle_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def enter_idle_state():
    global screen, state

    print("enter idle state")
    texture = pygame.Surface(screen.get_size()).convert()
    texture_rect = texture.get_rect()
    texture.fill(pygame.Color("black"))
    font = pygame.font.Font(None, 500)

    line_1 = font.render("Knopf", 1, (227, 157, 200))
    line_1_rect = line_1.get_rect()
    line_1_rect.centerx = texture_rect.centerx
    line_1_rect.centery = texture_rect.centery - int(line_1_rect.height / 2)
    texture.blit(line_1, line_1_rect)

    line_2 = font.render("drücken!", 1, (227, 157, 200))
    line_2_rect = line_2.get_rect()
    line_2_rect.centerx = texture_rect.centerx
    line_2_rect.centery = texture_rect.centery + int(line_2_rect.height / 2)
    texture.blit(line_2, line_2_rect)

    screen.blit(texture, (0, 0))
    pygame.display.flip()
    state = STATE_IDLE

Thread(target=main).start()

STATE_IDLE = 10
STATE_SHOWING_PHOTO = 20
