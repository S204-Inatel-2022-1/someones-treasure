import pygame as pg
from source.model.player import Player


def display_direction(player: Player):
    display_surface = pg.display.get_surface()
    font = pg.font.SysFont("Arial", 30)
    debug_surf = font.render(str(player.direction), True, "green")
    debug_rect = debug_surf.get_rect(topleft=(10, 10))
    pg.draw.rect(display_surface, "green", debug_rect, 1)
    display_surface.blit(debug_surf, debug_rect)


def display_grid():
    # This function display squares of 64 pixels on the screen
    display_surface = pg.display.get_surface()
    for i in range(0, display_surface.get_width(), 64):
        pg.draw.line(display_surface, "green", (i, 0),
                     (i, display_surface.get_height()))
    for i in range(0, display_surface.get_height(), 64):
        pg.draw.line(display_surface, "green", (0, i),
                     (display_surface.get_width(), i))
