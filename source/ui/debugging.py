'''
Contains methods for debugging.
'''
import pygame as pg


def display_info(info):
    '''
    Display information to the user.
    '''
    display_surface = pg.display.get_surface()
    width = display_surface.get_width()
    height = display_surface.get_height()
    font = pg.font.SysFont("Arial", 30)
    info_surface = font.render(str(info), True, "green")
    info_rect = info_surface.get_rect(bottomright=(width - 10, height - 10))
    pg.draw.rect(display_surface, "green", info_rect, 1)
    display_surface.blit(info_surface, info_rect)
