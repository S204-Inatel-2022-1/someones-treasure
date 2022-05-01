import pygame as pg
import sys
from source.utils.settings import RESOLUTION, FPS
from source.controller.map import Map


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.title = pg.display.set_caption("Someone's Treasure")
        img = pg.image.load("assets/images/game-icon.png").convert_alpha()
        self.icon = pg.display.set_icon(img)
        self.clock = pg.time.Clock()
        self.map = Map()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and
                                         event.key == pg.K_ESCAPE):
                self.running = False
                print("GAME OVER!\n")
                pg.quit()
                sys.exit()

    def _update(self):
        self.map.update()

    def _draw(self):
        self.screen.fill("black")
        self.map.draw()
        pg.display.flip()
