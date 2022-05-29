import pygame as pg
from scripts.constants import *


class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, style, surface=pg.surface.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.style = style
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        x_offset = y_offset = - TILE_SIZE // 4
        self.hitbox = self.rect.inflate(x_offset, y_offset)

    def break_tile(self):
        if self.style == "breakable":
            self.kill()
            sfx = pg.mixer.Sound(SFX["misc"]["break"])
