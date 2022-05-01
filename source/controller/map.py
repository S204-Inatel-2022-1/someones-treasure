import pygame as pg
from source.model.player import Player
from source.model.tile import Tile
from source.utils.manage_assets import get_layout, import_folder
from source.view.camera import Camera


class Map:
    def __init__(self):
        self.visible_sprites = Camera()
        self.obstacle_sprites = pg.sprite.Group()
        self.all_sprites = [self.visible_sprites, self.obstacle_sprites]
        self._render_map()

    def _render_map(self):
        layouts = {
            "boundary": get_layout("assets/data/map/Boundaries.csv"),
            "object": get_layout("assets/data/map/Objects.csv"),
            "player": get_layout("assets/data/map/Player.csv")
            # "wall": get_layout("assets/data/map/Walls.csv")
        }
        graphics = {
            "objects": import_folder("assets/images/graphics")
        }
        for style, layout in layouts.items():
            for y, tiles in enumerate(layout):
                for x, tile in enumerate(tiles):
                    if tile != "-1":
                        if style == "boundary":
                            Tile(self.obstacle_sprites, (x, y))
                        elif style == "object":
                            surface = graphics["objects"][int(tile)]
                            Tile(self.all_sprites, (x, y), surface)
                        elif style == "player":
                            self.player = Player(self.visible_sprites,
                                                 self.obstacle_sprites,
                                                 (x, y))

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()
