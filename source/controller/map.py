import pygame as pg
# from source.utils.settings import TILE_SIDE
from source.model.bomb import Bomb
from source.model.player import Player
from source.model.tile import Tile
from source.model.attack import Attack
from source.utils.asset_management import get_layout, import_folder
from source.view.camera import Camera


class Map:
    def __init__(self):
        self.visible_sprites = Camera()
        self.obstacle_sprites = pg.sprite.Group()
        self.all_sprites = [self.visible_sprites, self.obstacle_sprites]
        self._render_map()

    def _render_map(self):
        layouts = {
            "boundary": get_layout(f"assets/data/map/Boundaries.csv"),
            "object": get_layout(f"assets/data/map/Objects.csv"),
            "player": get_layout(f"assets/data/map/Player.csv")
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
                        elif style == "player":
                            self.player = Player(self.visible_sprites,
                                                 self.obstacle_sprites,
                                                 (x, y))
                        elif style == "object":
                            # print(tile)
                            # surface = graphics["objects"][int(tile)]
                            surface = graphics["objects"][0]
                            Tile(self.all_sprites, (x, y), surface)

    def draw(self):
        self.visible_sprites.custom_draw(self.player)

    def update(self):
        self.visible_sprites.update()

    '''
    def __place_bomb__(self):
        Bomb(self.player, [self.visible_sprites])
    '''
