'''
Contains the Tile class.
'''
from random import randint
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
        elif style != "boss_room":
            self.hitbox = self.rect.inflate(- TILE_SIZE // 4,
                                            - TILE_SIZE // 64)
        else:
            self.hitbox = self.rect.inflate(TILE_SIZE * 2, 0)

    @property
    def drop_ammo(self):
        '''
        Getter.
        '''
        return self.__drop_ammo

    @drop_ammo.setter
    def drop_ammo(self, function):
        '''
        Setter.
        '''
        self.__drop_ammo = function

    def break_tile(self):
        '''
        Method for breaking a tile.
        '''
        if self.style == "breakable":
            if self.is_crate:
                self.__drop_ammo(self.rect.center, 4)
            else:
                chance = randint(1, 100)
                if chance <= 25:
                    self.drop_ammo(self.rect.center, 1)
            sfx = pg.mixer.Sound(SFX["misc"]["break"])
            sfx.set_volume(0.3)
            sfx.play()
        self.kill()
