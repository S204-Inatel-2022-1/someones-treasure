import pygame as pg
import sys
from scripts.constants import *
from scripts.level import Level
from scripts.utils import clear_screen


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption("Someone's Treasure")
        icon = pg.image.load("images/icons/game-icon.png").convert_alpha()
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.level = Level()

    def play(self):
        while True:
            self.clock.tick(FPS)
            self.screen.fill("black")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.close()
                    if event.key == pg.K_RETURN:
                        if not self.level.game_over:
                            self.level.pause()
                        else:
                            self.level.reset()
            self.level.run()
            pg.display.update()

    def close(self):
        print("GAME OVER!\n")
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    clear_screen()
    game = Game()
    game.play()
