import pygame as pg
from source.helper.settings import TILE_SIZE

SIZE = TILE_SIZE, TILE_SIZE


class Tile(pg.sprite.Sprite):
    def __init__(self, position: tuple, sprites: pg.sprite.Group,
                 surface: pg.surface.Surface = pg.Surface(SIZE)):
        super().__init__(sprites)
        position = position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
