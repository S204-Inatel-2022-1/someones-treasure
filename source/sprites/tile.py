'''
Contains the Tile class.
'''

import pygame as pg

from source.constants.paths import SFX
from source.constants.settings import TILE_SIZE


class Tile(pg.sprite.Sprite):
    '''
    Class for basic tiles.
    '''

    def __init__(self, groups, pos, style, surface=pg.surface.Surface((TILE_SIZE, TILE_SIZE)), is_crate=False):
        super().__init__(groups)
        self.style = style
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.is_crate = is_crate
        if style != "hole":
            self.hitbox = self.rect.inflate(- TILE_SIZE // 4,
                                            - TILE_SIZE // 4)
        else:
            self.hitbox = self.rect.inflate(- TILE_SIZE // 4,
                                            - TILE_SIZE // 64)

    def break_tile(self):
        '''
        Method for breaking a tile.
        '''
        if self.style == "breakable":
            if self.is_crate:
                # Drops 8 Ammo =)
                pass
            self.kill()
            sfx = pg.mixer.Sound(SFX["misc"]["break"])
            sfx.set_volume(0.3)
            sfx.play()
