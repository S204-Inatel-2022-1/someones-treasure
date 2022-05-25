import pygame as pg
from random import choice
from scripts.camera import Camera
from scripts.constants import *
from scripts.monster import Monster
from scripts.player import Player
from scripts.tile import Tile
from scripts.utils import import_folder, import_layout
from scripts.ui import UserInterface


class Level:
    def __init__(self):
        self.visible_sprites = Camera()
        self.obstacle_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()
        self.paused = False
        self.__render_map()
        pg.mixer.init()
        pg.mixer.music.load(MUSIC["main_loop"])
        pg.mixer.music.play(-1)
        self.game_over_music = pg.mixer.Sound(MUSIC["game_over"])
        self.game_over_music.set_volume(0.5)
        self.game_over = False

    def __render_map(self):
        layouts = {
            "boundary": import_layout(f"data/map_Boundaries.csv"),
            # "breakable": import_layout(f"data/map_Breakable.csv"),
            "entity": import_layout(f"data/map_Entities.csv"),
            "object": import_layout(f"data/map_Objects.csv")
        }
        graphics = {
            # "breakable": import_folder("assets/images/breakable"),
            "objects": import_folder("images/objects")
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != "-1":
                        x = j * TILE_SIZE
                        y = i * TILE_SIZE
                        pos = x, y
                        if style == "boundary":
                            groups = [self.obstacle_sprites]
                            Tile(groups, pos, style)
                        elif style == "breakable":
                            '''
                            random_stuff = choice(graphics["breakable"])
                            groups = [self.visible_sprites,
                                      self.obstacle_sprites,
                                      self.__attackable_sprites]
                            Tile(groups, pos, style, random_stuff)
                            '''
                            pass
                        elif style == "entity":
                            if col != "65":
                                monster_name = "rat"
                                """
                                if col == "66":
                                    monster_name = "skeleton"
                                elif col == "67":
                                    monster_name = "ghost"
                                elif col == "68":
                                    monster_name = "slime"
                                else:
                                    monster_name = "rat"
                                """
                                groups = [self.visible_sprites,
                                          self.attackable_sprites]
                                obstacles = self.obstacle_sprites
                                Monster(groups, obstacles, pos, monster_name,
                                        self._damage_player)
                            else:
                                groups = [self.visible_sprites]
                                obstacles = self.obstacle_sprites
                                self.player = Player(groups, obstacles, pos)
                                self.ui = UserInterface(self.player)
                        elif style == "object":
                            surface = graphics["objects"][int(col)]
                            groups = [self.visible_sprites,
                                      self.obstacle_sprites]
                            Tile(groups, pos, style, surface)

    def run(self):
        if self.player.hp > 0:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            if self.paused:
                self.ui.display_pause()
            else:
                self.visible_sprites.update()
                self.visible_sprites.update_monsters(self.player)
                # self.attack_logic()
        else:
            self.ui.display_game_over()
            if not self.game_over:
                pg.mixer.music.stop()
                self.game_over_music.play()
                self.game_over = True

    def pause(self):
        if self.paused:
            pg.mixer.music.unpause()
            self.paused = False
        else:
            pg.mixer.music.pause()
            self.paused = True

    def _damage_player(self, amount):
        self.player.take_damage(amount)

    def reset(self):
        self.__init__()
