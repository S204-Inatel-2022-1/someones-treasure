from csv import reader
from PIL import Image
import numpy as np
import pygame as pg
import os

from scripts.constants import TILE_SIZE


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("Press 'ENTER' to continue...")


def import_folder(path):
    surfaces = []
    files = os.listdir(path)
    for num in range(len(files)):
        surface = pg.image.load(f"{path}/{num}.png").convert_alpha()
        surfaces.append(surface)
    return surfaces


def import_layout(path):
    layout = []
    with open(path) as level_map:
        map = reader(level_map, delimiter=",")
        for tile in map:
            layout.append(list(tile))
        return layout


def crop_tileset():
    image = Image.open("images/tile/tileset.png")
    image_array = np.array(image)
    count = 0
    width, height = image.size
    for row in range(0, height, TILE_SIZE):
        for col in range(0, width, TILE_SIZE):
            array = np.copy(image_array)
            array = array[row:row + TILE_SIZE, col:col + TILE_SIZE]
            cropped_image = Image.fromarray(array)
            cropped_image.save(f"images/objects/{count}.png")
            count += 1
