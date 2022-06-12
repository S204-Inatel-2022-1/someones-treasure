import pygame as pg
from source.constants.settings import TILE_SIZE


class HealthBar:
    def __init__(self, hp, max_hp):
        self.display_surface = pg.display.get_surface()
        self.hp = hp
        self.max_hp = max_hp
        self.__import_graphics()

    def __import_graphics(self):
        self.hearts = []
        for i in range(0, self.max_hp + 1):
            image = f"images/hp/{self.max_hp}/{str(i)}.png"
            self.hearts.append(pg.image.load(image).convert_alpha())
        self.image = self.hearts[self.hp]
        self.rect = self.image.get_rect(topleft=(TILE_SIZE // 4,
                                                 TILE_SIZE // 4))

    def display(self, hp, max_hp):
        if max_hp != self.max_hp:
            self.__update_max_hp(max_hp)
        if hp != self.hp:
            self.hp = hp
            self.image = self.hearts[self.hp]
        self.display_surface.blit(self.image, self.rect)

    def __update_max_hp(self, max_hp):
        self.max_hp = max_hp
        self.__import_graphics()
