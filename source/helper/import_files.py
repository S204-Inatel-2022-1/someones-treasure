from csv import reader
from os import walk
import pygame as pg


def import_folder(filename):
    surface_list = []
    for _, __, img_files in walk(filename):
        for image in img_files:
            full_path = filename + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def import_layout(filename):
    terrain_map = []
    with open(filename, "r") as map:
        layout = reader(map)
        for tile in layout:
            terrain_map.append(list(tile))
        return terrain_map
