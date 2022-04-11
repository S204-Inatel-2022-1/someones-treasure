import pygame as pg
from source.helper.import_assets import get_layout, get_folder
from source.helper.settings import TILE_SIZE
from source.model.player import Player
from source.model.tile import Tile
from source.view.camera import Camera


class Level(object):
    def __init__(self, current_lvl: int):
        self.visible_sprites = Camera()
        self.obstacle_sprites = pg.sprite.Group()
        self.sprites = [self.visible_sprites, self.obstacle_sprites]
        self.index = current_lvl
        self.__render_map__()

    def __render_map__(self):
        layouts = {
            "boundary": get_layout("assets/data/levels/0/level_0_boundaries.csv"),
            "ceil": get_layout("assets/data/levels/0/level_0_ceil.csv"),
            "object": get_layout("assets/data/levels/0/level_0_objects.csv")
        }
        graphics = {
            "ceil": get_folder("assets/images/graphics/ceil"),
            "objects": get_folder("assets/images/graphics/objects")
        }
        for style, layout in layouts.items():
            for y, tiles in enumerate(layout):
                for x, tile in enumerate(tiles):
                    if tile != "-1":
                        # x, y = i * TILE_SIZE, j * TILE_SIZE
                        if style == "boundary":
                            Tile(
                                (x, y), [self.obstacle_sprites], "invisible")
                        elif style == "object":
                            surface = graphics["objects"][int(tile)]
                            Tile(
                                (x, y), [self.visible_sprites, self.obstacle_sprites], "object", surface)
                        elif style == "ceil":
                            surface = graphics["ceil"][int(tile)]
                            Tile((x, y), [self.visible_sprites,
                                            self.obstacle_sprites], "ceil", surface)
            self.player = Player((13, 5), [self.visible_sprites],
                                 self.obstacle_sprites)

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()
        # self.player.update()
