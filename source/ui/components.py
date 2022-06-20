'''
Contains the components for the Player UI.
'''
import pygame as pg

from source.constants.paths import FONT
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
        self.font = pg.font.Font(FONT, 24)
        self.__update_text()

    def __import_graphics(self):
        self.image = pg.image.load("images/projectile/ammo.png")
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
            self.update_max_ammo(max_ammo)
        if ammo != self.ammo:
            self.ammo = ammo
            self.__update_text()
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.text, (TILE_SIZE + 10, TILE_SIZE + 10))

    def update_max_ammo(self, max_ammo):
        '''
        Updates the max ammo.
        '''
        self.max_ammo = max_ammo
        self.__update_text()
        self.__import_graphics()


class HealthBar:
    '''
    Class to display the player's health.
    '''

    def __init__(self, health, max_health):
        self.display_surface = pg.display.get_surface()
        self.health = max(health, 0)
        self.max_health = max_health
        self.hearts = self.__import_graphics()
        # print("~ ~ ~ HP FLAG =", health, max_health, len(self.hearts))
        self.image = self.hearts[self.health]
        position = TILE_SIZE // 4, TILE_SIZE // 4
        self.rect = self.image.get_rect(topleft=position)

    def __import_graphics(self):
        hearts = []
        for i in range(0, self.max_health + 1):
            image = f"images/hp/{self.max_health}/{str(i)}.png"
            hearts.append(pg.image.load(image).convert_alpha())
        return hearts

    def display(self, health, max_health):
        '''
        Display the player's health.
        '''
        if max_health != self.max_health:
            self.update_max_health(max_health)
        if health != self.health:
            self.health = max(health, 0)
            self.image = self.hearts[self.health]
        self.display_surface.blit(self.image, self.rect)

    def update_max_health(self, max_health):
        '''
        Updates the max health.
        '''
        self.max_health = max_health
        self.hearts = self.__import_graphics()
