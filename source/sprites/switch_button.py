'''
Contains the SwitchButton class.
'''
import pygame as pg

from source.constants.paths import SFX


class SwitchButton(pg.sprite.Sprite):
    '''
    Controls the toggle of some special walls.
    '''

    def __init__(self, groups, pos, piston_walls):
        super().__init__(groups)
        self.toggle_value = 0
        self.piston_walls = piston_walls
        self.image = self.__import_graphics()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

    @property
    def activate_pistons(self):
        '''
        Returns the function.
        '''
        return self.__activate_pistons

    @activate_pistons.setter
    def activate_pistons(self, function):
        self.__activate_pistons = function

    def __import_graphics(self):
        '''
        Import the graphics for the switch.
        '''
        image = pg.image.load(f"images/switch/{self.toggle_value}.png")
        return image

    def update(self):
        '''
        Basic update method.
        '''

    def toggle(self):
        '''
        Toggle the value of the switch.
        '''
        self.toggle_value = 1
        self.image = self.__import_graphics()
        self.activate_pistons()
        sfx = pg.mixer.Sound(SFX["misc"]["hit"])
        sfx.set_volume(0.3)
        sfx.play()
