import pygame as pg
import sys
from source.constants.settings import *
from source.logic.level import Level
from source.logic.utils import clear_console


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION, pg.RESIZABLE)
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
                            self.level.restart()
            self.level.run()
            pg.display.update()

    def close(self):
        print("GAME OVER!\n")
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    clear_console()
    game = Game()
    game.play()
