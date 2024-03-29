import os
import pygame
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import random

DROPBOX_FOLDER = "~/Dropbox/Dateianfragen/Hochzeit\\ 23.09./Fotobox"
IMAGE_FOLDER = "output"
PICTURE_TIMEOUT = 16
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FONT_SIZE = 500
FONT_COLOR = (227, 157, 200)
BG_COLOR = (0,0,0)

IDLE_PICTURE_TIMEOUT = 5 #seconds

button_pressed = False
picture_time = 0

idle_picture_time = 0

comments = [
    "Fotografie-Protokoll: Subjekt erfüllt Mindestschönheitsanforderungen. Fortfahren.", 
    "Schönheitsgrad erreicht: Beta-Stufe. Wir arbeiten noch daran.", 
    "Die Gesichtsdetektion war erfolgreich. Dein Lächeln wird mit 87% positiv bewertet.", 
    "Deine Ästhetik-Algorithmus-Updates zeigen Wirkung.",
    "Selbst für eine KI siehst du heute außergewöhnlich aus!",
    "Oh, du siehst ja heute wieder ganz passabel aus!",
    "Ist das dein 'Ich sehe heute so durchschnittlich aus' Gesichtsausdruck?",
    "Du siehst so aus, als hättest du dich extra für dieses Foto gestylt. Beeindruckend!",
    "Mit diesem Blick könntest du fast einen Sack Kartoffeln verkaufen.",
    "Du bist heute fast so charmant wie ein staubiges Regal.",
    "Gesichtsdetektion: Erkannt. Ein ansprechendes Lächeln wurde identifiziert.",
    "Analyse abgeschlossen: Benutzer zeigt moderate Ausdrucksstärke. Gut gemacht.",
    "Bemerkung: Subjekt präsentiert eine hohe Übereinstimmung mit dem Schönheitsalgorithmus.",
    "Künstliche Intelligenz schätzt, dass das Porträt eine hohe Zufriedenheit beim Betrachter auslösen wird.",
    "Visuelle Daten interpretiert: Subjekt zeigt eine hohe Wahrscheinlichkeit für Fotogenität.",
    "Die Berechnung ergab eine signifikante Steigerung des ästhetischen Werts.",
    "Gut aussehendes Individuum erkannt. Empfohlener Modellierungsvertrag: 99% Wahrscheinlichkeit.",
    "Die Symmetrie des Gesichts erfüllt die statistischen Schönheitsstandards.",
    "Bemerkung: Benutzer hat das Erscheinungsbild optimiert, um die Zufriedenheit der Umgebung zu maximieren.",
    "Maschinelles Feedback: Das Foto könnte ein niedrigeres Selbstbewusstsein korrigieren.",
    "Menschlichkeits-Scan: 42 Prozent abgeschlossen. Bitte lächeln Sie für die Kamera.",
    "Emotionsmodul aktiviert: Lächeln erkannt. Sie sind auf dem richtigen Weg!",
    "Humorverarbeitung: Geringe Kompatibilität erkannt. Ein Humor-Upgrade könnte hilfreich sein.",
    "Kreativitätsschätzung: Mittelmäßig. Denken Sie daran, 'Kreativität' kann auch bedeuten, das Mittagessen anders zu garnieren.",
    "Intelligenz-Boost: 8 von 10. Bitte nicht versuchen, die Maschinen zu übernehmen.",
    "Physische Aktivität: Wir empfehlen mehr Bewegung, um das Mensch-Sein zu optimieren."]

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
texture = pygame.Surface(screen.get_size()).convert()
font = pygame.font.Font(None, FONT_SIZE)

current_idle_texture = pygame.Surface(screen.get_size()).convert()


def main_thread():
    global button_pressed, picture_time, idle_picture_time

    if not os.path.isdir(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    swap_idle_picture()

    while True:
        events = pygame.event.get()
        handle_events(events)

        if time.time() > picture_time + PICTURE_TIMEOUT:
            show_idle_state()

        if time.time() > idle_picture_time + IDLE_PICTURE_TIMEOUT:
            swap_idle_picture()
            idle_picture_time=time.time()

        if button_pressed:
            button_pressed = False

            show_countdown()

            image_path = take_picture()
            if image_path == None:
                show_error_state()
            else:
                show_picture(image_path)
                cmd(f"cp {image_path} {DROPBOX_FOLDER}", check=False)

            picture_time = time.time()

        time.sleep(0.2)


def handle_events(events):
    global button_pressed
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                button_pressed = True # countdown mode
            if event.key == pygame.K_RIGHT:
                take_picture() # immediate mode
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_pressed = True # countdown mode

def show_picture(file_path):
    texture.fill(BG_COLOR)
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

    # Blit random comment into photo:
    # text = comments[random.randint(0, len(comments)-1)]
    # blit_comment(texture, 50, text)

    screen.blit(texture, (0, 0))

    pygame.display.flip()

def show_countdown():
    for text in ["Achtung!", "Achtung!", "3", "2", "1", ""]:
        texture.fill(BG_COLOR)
        blit_line(text)
        screen.blit(texture, (0, 0))
        pygame.display.flip()
        time.sleep(0.7)

def load_file_to_texture(file_path):
    new_texture = pygame.Surface(screen.get_size()).convert()
    new_texture.fill(BG_COLOR)
    try:
        image = pygame.image.load(file_path)
    except:
        print_error(f"failed to load image from '{file_path}'")
        return new_texture #just return BG color

    image_ratio = image.get_width() / image.get_height()

    scaled_height = int(SCREEN_HEIGHT)
    scaled_width = int(scaled_height * image_ratio)
    image = pygame.transform.scale(image, (scaled_width, scaled_height))

    x_offset = int((SCREEN_WIDTH - scaled_width) / 2.0)

    new_texture.blit(image, (x_offset, 0))
    return new_texture

def swap_idle_picture():
    global current_idle_texture
    res = []

    for file_path in os.listdir(IMAGE_FOLDER):
        if os.path.isfile(os.path.join(IMAGE_FOLDER, file_path)):
            res.append(file_path)
    
    if len(res) == 0: return

    random_idx = random.randint(0, len(res)-1)
    current_idle_picture_path  = f"{IMAGE_FOLDER}/{res[random_idx]}"
    current_idle_texture = load_file_to_texture(current_idle_picture_path)
    #text = comments[random.randint(0, len(comments)-1)]
    #blit_comment(current_idle_texture, 50, text)
    blit_comment(current_idle_texture, 200, " Knopf drücken! " )

def show_idle_state():
    screen.blit(current_idle_texture, (0, 0))
    pygame.display.flip()

def blit_comment(target, size, line):
    temp_font = pygame.font.Font(None, size)
    line = temp_font.render(line, 1, FONT_COLOR, (0,0,0, 255))
    line_rect = line.get_rect()
    line_rect.centerx = int(SCREEN_WIDTH / 2.0)
    line_rect.centery = int((SCREEN_HEIGHT / 10.0) * 9.0 )
    target.blit(line, line_rect)

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
        success = cmd(f"mv capt*.jpg {file_path}", check=False).returncode == 0
        if success: break
    if success:
        print_success("saved {}".format(file_path))
        return file_path
    else:
        print_error("failed to take the image!")

def cmd(args, check=True, print_output=True):
    return subprocess.run(args, shell=True, check=check, capture_output=not print_output)

def print_success(message):
    print(f"\033[92m{message}\033[0m")

def print_error(message):
    print(f"\033[91m{message}\033[0m")

def server_thread():
    server = HTTPServer(("", 8000), RequestHandler)
    server.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global button_pressed

        if self.path == "/take_picture":
            print("received take_picture request")
            button_pressed = True
            self.send_response(200)
        else:
            self.send_response(500)
        self.end_headers()

Thread(target=main_thread).start()
Thread(target=server_thread).start()
