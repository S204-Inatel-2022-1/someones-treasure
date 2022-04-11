from csv import reader
from os import walk
import pygame as pg


def get_folder(path: str):
    surfaces = []
    for _, __, files in walk(path):
        for image in files:
            file_name = path + "/" + image
            surface = pg.image.load(file_name).convert_alpha()
            surfaces.append(surface)
    return surfaces


def get_layout(path: str):
    map_layout = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for tile in layout:
            map_layout.append(list(tile))
        return map_layout
