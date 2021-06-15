import pygame
import sys
import random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME


def game_quit():
    pygame.quit()
    sys.exit()


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('cannot load an image')
        raise SystemExit(message)
    image = image.convert_alpha()
    return image, image.get_rect()


pygame.init()

window_width = 1024
window_height = 768
surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('later bitches')
clock = GAME_TIME.Clock()

while True:

    surface.fill((0, 0, 0))

    clock.tick(30)
    pygame.display.update()

    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            game_quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_quit()
