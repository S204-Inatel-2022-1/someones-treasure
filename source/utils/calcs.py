import pygame as pg
from source.constants.settings import TILE_SIZE


def calculate_relative_vector(own_rect, another_rect):
    another_vector = pg.math.Vector2(another_rect.center)
    own_vector = pg.math.Vector2(own_rect.center)
    vector = another_vector - own_vector
    return vector


def calculate_relative_distance(own_rect, another_rect):
    vector = calculate_relative_vector(own_rect, another_rect)
    distance = vector.magnitude()
    return distance


def calculate_relative_direction(own_rect, another_rect):
    distance = calculate_relative_distance(own_rect, another_rect)
    if distance > 0:
        vector = calculate_relative_vector(own_rect, another_rect)
        direction = vector.normalize()
    else:
        direction = pg.math.Vector2(0, 0)
    return direction


def calculate_half_dimensions():
    display_surface = pg.display.get_surface()
    half_width = display_surface.get_width() // 2
    half_height = display_surface.get_height() // 2
    return half_width, half_height


def calculate_screen_vector(half_width, half_height):
    return pg.math.Vector2(half_width + TILE_SIZE, half_height + TILE_SIZE)
