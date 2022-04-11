import pygame as pg
from source.helper.import_assets import get_layout, get_folder
from source.helper.settings import TILE_SIZE
from source.model.player import Player
from source.model.tile import Tile
from source.view.camera import Camera


class Level(object):
    def __init__(self, current_lvl: int):
        self.visible_sprites = Camera(current_lvl)
        self.obstacle_sprites = pg.sprite.Group()
        self.sprites = [self.visible_sprites, self.obstacle_sprites]
        self.index = current_lvl
        self.__render_map__()

    def __render_map__(self):
        layouts = {
            "boundary": get_layout(f"assets/data/levels/{self.index}/{self.index}_Boundaries.csv"),
            "object": get_layout(f"assets/data/levels/{self.index}/{self.index}_Objects.csv"),
            "player": get_layout(f"assets/data/levels/{self.index}/{self.index}_Player.csv")
        }
        graphics = {
            "objects": get_folder("assets/images/graphics/objects")
        }
        for style, layout in layouts.items():
            for y, tiles in enumerate(layout):
                for x, tile in enumerate(tiles):
                    if tile != "-1":
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites])
                        if style == "object":
                            surface = graphics["objects"][int(tile)]
                            Tile((x, y), self.sprites, surface)
                        elif style == "player":
                            self.player = Player((x, y),
                                                 [self.visible_sprites],
                                                 self.obstacle_sprites)
                        elif style == "shadow":
                            surface = graphics["shadows"][int(tile)]
                            Tile((x, y), self.sprites, surface, False)
                        elif style == "wall":
                            surface = graphics["walls"][int(tile)]
                            Tile((x, y), self.sprites, surface)

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()
