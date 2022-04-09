import pygame as pg
from source.controller.settings import TILE_SIZE


class Tile(pg.sprite.Sprite):
    def __init__(self, position: tuple, groups: pg.sprite.Group(), sprite_type: str,
                 surface=pg.Surface((TILE_SIZE, TILE_SIZE)), image_path: str = None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "suamae":  # or sprite_type == "ceil":
            x, y = position[0], position[1] - TILE_SIZE
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
