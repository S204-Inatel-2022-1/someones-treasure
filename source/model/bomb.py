import pygame as pg
from source.model.tile import Tile
from source.utils.settings import TILE_SIZE

'''
This Class will be translated into a TNT barrel or something like that.
'''


class Bomb(Tile):
    def __init__(self, groups, pos):
        super().__init__(groups, pos)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-32, -32)

    def detonate(self):
        self.kill()
