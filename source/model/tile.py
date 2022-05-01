import numpy as np
import pygame as pg
from source.utils.settings import TILE_SIZE


class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, surface=pg.surface.Surface((TILE_SIZE, TILE_SIZE)), has_collision=False):
        super().__init__(groups)
        pos = np.multiply(pos, TILE_SIZE)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(- TILE_SIZE // 16, - TILE_SIZE // 4)
