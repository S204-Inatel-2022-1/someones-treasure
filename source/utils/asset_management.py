from csv import reader
from os import walk
import pygame as pg


def import_folder(path: str):
    surfaces = []
    for _, __, files in walk(path):
        for image in files:
            full_path = path + "/" + image
            surface = pg.image.load(full_path).convert_alpha()
            surfaces.append(surface)
    return surfaces


def get_layout(path: str):
    layout = []
    with open(path) as level_map:
        map = reader(level_map, delimiter=",")
        for tile in map:
            layout.append(list(tile))
        return layout
