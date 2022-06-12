import pygame as pg
from source.constants.settings import TILE_SIZE


class AmmoBar:
    def __init__(self, ammo, max_ammo):
        self.display_surface = pg.display.get_surface()
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.__import_graphics()
        self.font = pg.font.Font("fonts/PixelGameFont.ttf", 24)
        self.__update_text()

    def __import_graphics(self):
        self.image = pg.image.load(f"images/projectile/right.png")
        x, y = TILE_SIZE // 4, TILE_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def __update_text(self):
        self.text = self.font.render(f"{self.ammo}/{self.max_ammo}",
                                     False, "white")

    def display(self, ammo, max_ammo):
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
