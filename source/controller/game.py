import pygame as pg
import sys
from source.controller.settings import *
from source.model.level import Level
from source.tests.debug import display_grid


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(RESOLUTION)
        self.title = pg.display.set_caption("Someone's Treasure")
        img = pg.image.load("assets/images/icon.png").convert_alpha()
        self.icon = pg.display.set_icon(img)
        self.clock = pg.time.Clock()
        self.fps = FPS
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.level.update()
        pass

    def draw(self):
        self.screen.fill("#42393a")
        self.level.draw()
        # display_grid()
        pg.display.flip()
