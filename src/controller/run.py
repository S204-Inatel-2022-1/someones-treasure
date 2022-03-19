import pygame
import sys
from src.helper.console_control import cls
from src.helper.settings import FPS
from src.model.game import Game


def run():
    cls()
    pygame.init()
    new_game = Game()
    while new_game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Game closed!')
                pygame.quit()
                sys.exit()
        new_game.window.fill('green')
        # self.level.start_lvl()
        pygame.display.update()
        new_game.clock.tick(FPS)
