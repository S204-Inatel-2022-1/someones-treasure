'''
Contains functions to manage the game's assets.
'''
from csv import reader
from os import listdir
from PIL import Image
import numpy as np
import pygame as pg

from source.constants.settings import TILE_SIZE


def import_folder(path):
    '''
    Imports all images in a folder.
    '''
    surfaces = []
    files = listdir(path)
    for num in range(len(files)):
        surface = pg.image.load(f"{path}/{num}.png").convert_alpha()
        surfaces.append(surface)
    return surfaces


def import_layout(path):
    '''
    Imports a map layout from a CSV file.
    '''
    layout = []
    with open(path, encoding="utf-8") as level_map:
        map_ = reader(level_map, delimiter=",")
        for tile in map_:
            layout.append(list(tile))
        return layout


def crop_tileset():
    '''
    Don't use this function. It was created just to help me crop the tileset faster.
    '''
    image = Image.open("images/tile/tileset.png")
    image_array = np.array(image)
    count = 0
    width, height = image.size
    for row in range(0, height, TILE_SIZE):
        for col in range(0, width, TILE_SIZE):
            array = np.copy(image_array)
            array = array[row:row + TILE_SIZE, col:col + TILE_SIZE]
            cropped_image = Image.fromarray(array)
            cropped_image.save(f"images/tileset/{count}.png")
            count += 1
