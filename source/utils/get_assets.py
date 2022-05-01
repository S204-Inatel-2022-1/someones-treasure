from csv import reader
from os import listdir
import pygame as pg


def import_folder(path):
    surfaces = []
    files = listdir(path)
    num_of_files = len(files)
    for num in range(num_of_files):
        full_path = f"{path}/{num}.png"
        surface = pg.image.load(full_path).convert_alpha()
        surfaces.append(surface)
    return surfaces


def get_layout(path):
    layout = []
    with open(path) as level_map:
        map = reader(level_map, delimiter=",")
        for tile in map:
            layout.append(list(tile))
        return layout
