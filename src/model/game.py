from cProfile import run
import pygame as pg
import sys
from src.controller.settings import *
from src.model.level import Level


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        file = 'assets/img/misc/game_icon.png'
        pg.display.set_icon(pg.image.load(file).convert_alpha())
        self.level = Level()
        self.running = True

    def start(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.fill(CUSTOM_COLOR)
            self.level.run()
            pg.display.update()
            self.clock.tick(60)
