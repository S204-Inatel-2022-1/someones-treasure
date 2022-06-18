'''
Contains some methods mainly used for calculation in other parts of the code.
'''
import pygame as pg


def rel_vector(own_rect, another_rect):
    '''
    Calculates the relative vector from one sprite to another.
    '''
    another_vector = pg.math.Vector2(another_rect.center)
    own_vector = pg.math.Vector2(own_rect.center)
    vector = another_vector - own_vector
    return vector


def rel_distance(own_rect, another_rect):
    '''
    Calculates the relative distance from one sprite to another.
    '''
    vector = rel_vector(own_rect, another_rect)
    distance = vector.magnitude()
    return distance


def rel_direction(own_rect, another_rect):
    '''
    Calculates a direction vector from one sprite to another.
    '''
    distance = rel_distance(own_rect, another_rect)
    if distance > 0:
        vector = rel_vector(own_rect, another_rect)
        direction = vector.normalize()
    else:
        direction = pg.math.Vector2(0, 0)
    return direction


def half_dimensions():
    '''
    Calculates screen dimensions divided by two.
    '''
    display_surface = pg.display.get_surface()
    half_width = display_surface.get_width() // 2
    half_height = display_surface.get_height() // 2
    return half_width, half_height
