'''
Contains the components for the Player UI.
'''
import pygame as pg
from source.constants.settings import TILE_SIZE


class AmmoBar:
    '''
    Class to display the player's ammo.
    '''

    def __init__(self, ammo, max_ammo):
        self.display_surface = pg.display.get_surface()
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.__import_graphics()
        self.font = pg.font.Font("fonts/PixelGameFont.ttf", 24)
        self.__update_text()

    def __import_graphics(self):
        self.image = pg.image.load("images/projectile/right.png")
        x, y = TILE_SIZE // 4, TILE_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def __update_text(self):
        ammo_comparison = f"{self.ammo}/{self.max_ammo}"
        self.text = self.font.render(ammo_comparison, False, "white")

    def display(self, ammo, max_ammo):
        '''
        Display the player's ammo.
        '''
        if max_ammo != self.max_ammo:
            self.__update_max_ammo(max_ammo)
        if ammo != self.ammo:
            self.ammo = ammo
            self.__update_text()
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.text, (TILE_SIZE, TILE_SIZE))

    def __update_max_ammo(self, max_ammo):
        self.max_ammo = max_ammo
        self.__update_text()
        self.__import_graphics()


class HealthBar:
    '''
    Class to display the player's health.
    '''

    def __init__(self, hp_, max_hp):
        self.display_surface = pg.display.get_surface()
        self.hp_ = hp_
        self.max_hp = max_hp
        self.__import_graphics()
        self.image = self.hearts[self.hp_]
        position = TILE_SIZE // 4, TILE_SIZE // 4
        self.rect = self.image.get_rect(topleft=position)

    def __import_graphics(self):
        self.hearts = []
        for i in range(0, self.max_hp + 1):
            image = f"images/hp/{self.max_hp}/{str(i)}.png"
            self.hearts.append(pg.image.load(image).convert_alpha())

    def display(self, hp_, max_hp):
        '''
        Display the player's health.
        '''
        if max_hp != self.max_hp:
            self.__update_max_hp(max_hp)
        if hp_ != self.hp_:
            self.hp_ = hp_
            self.image = self.hearts[self.hp_]
        self.display_surface.blit(self.image, self.rect)

    def __update_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.__import_graphics()
