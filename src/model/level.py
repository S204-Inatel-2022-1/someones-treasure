import pygame as pg
from src.controller.settings import *
from src.model.tile import Tile
from src.model.player import Player
from src.model.camera import YSortCameraGroup


class Level():
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacles = pg.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(OVERWORLD):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites],
                                         self.obstacles)

    def run(self):
        # Draw and update the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
