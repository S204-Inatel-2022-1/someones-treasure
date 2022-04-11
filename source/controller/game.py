import pygame as pg
import sys
from source.helper.settings import RESOLUTION, FPS
from source.view.level import Level


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.title = pg.display.set_caption("Someone's Treasure")
        img_path = "assets/images/icon.png"
        img = pg.image.load(img_path).convert_alpha()
        self.icon = pg.display.set_icon(img)
        self.clock = pg.time.Clock()
        self.level = Level(0)

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.__set_events__()
            self.__update__()
            self.__draw__()

    def __set_events__(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                print("GAME OVER!\n")
                pg.quit()
                sys.exit()

    def __update__(self):
        self.level.update()

    def __draw__(self):
        self.screen.fill("black")
        self.level.draw()
        pg.display.flip()
