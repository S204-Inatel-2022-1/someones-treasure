import pygame
from src.helper.settings import WINDOW_SIZE


class Game():
    def __init__(self):
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Someone's Treasure")
        file_name = 'assets/img/sprites/game_icon.png'
        pygame.display.set_icon(pygame.image.load(file_name).convert_alpha())
        # Hm...
        self.clock = pygame.time.Clock()
        self.running = True
