import pygame
import sys
from game.controller.settings import *


def start_game():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    title_font = pygame.font.Font('assets/fonts/PixelGameFont.ttf', 64)
    title = pygame.display.set_caption(TITLE)

    icon_surf = pygame.image.load(
        'assets/images/misc/game_icon.png').convert_alpha()
    icon = pygame.display.set_icon(icon_surf)

    current_state = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)
