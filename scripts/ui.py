import pygame as pg

from scripts.constants import *


class UserInterface:
    def __init__(self, player):
        self.hp_bar = HealthBar(player.hp, player.stats["hp"])
        self.ammo_ui = AmmoUI(player.ammo, player.stats["ammo"])
        self.pause_screen = PauseScreen()

    def display(self, player):
        self.hp_bar.display(player.hp, player.stats["hp"])
        self.ammo_ui.display(player.ammo, player.stats["ammo"])

    def display_pause(self):
        self.pause_screen.display()


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


class AmmoUI:
    def __init__(self, ammo, max_ammo):
        self.display_surface = pg.display.get_surface()
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.__import_graphics()
        self.font = pg.font.SysFont("fonts/PixelGameFont.ttf", 36)
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


class PauseScreen:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.SysFont("fonts/PixelGameFont.ttf", 36)
        self.text = self.font.render("PAUSED", False, "white")
        self.rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def display(self):
        self.display_surface.blit(self.text, self.rect)
