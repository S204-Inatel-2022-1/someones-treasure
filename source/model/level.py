import pygame as pg
from source.controller.settings import TILE_SIZE
from source.helper.import_files import import_layout, import_folder
from source.model.enemy import Enemy
from source.model.player import Player
from source.model.tile import Tile
from source.view.camera import Camera


class Level:
    def __init__(self):
        # self.display_surface = pg.display.get_surface()
        self.visible_sprites = Camera()
        self.obstacle_sprites = pg.sprite.Group()
        self.all_sprites = [self.visible_sprites, self.obstacle_sprites]
        self.player = None
        self.render_map()

    def render_map(self):
        layouts = {
            "boundary": import_layout("source/data/levels/0/level_0_boundaries.csv"),
            "ceil": import_layout("source/data/levels/0/level_0_ceil.csv"),
            "object": import_layout("source/data/levels/0/level_0_objects.csv")
        }
        graphics = {
            "ceil": import_folder("assets/images/graphics/ceil"),
            "objects": import_folder("assets/images/graphics/objects")
        }
        for style, layout in layouts.items():
            for j, tiles in enumerate(layout):
                for i, tile in enumerate(tiles):
                    if tile != "-1":
                        x, y = i * TILE_SIZE, j * TILE_SIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        elif style == "object":
                            print(f"Tile = {int(tile)}\nx, y = {i}, {j}")
                            surface = graphics["objects"][int(tile)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                 "object", surface)
                        elif style == "ceil":
                            surface = graphics["ceil"][int(tile)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                 "ceil", surface)
                    '''
                    '''
        self.player = Player((13 * TILE_SIZE, 5 * TILE_SIZE), self.visible_sprites,
                             self.obstacle_sprites)

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()
        self.player.update()
