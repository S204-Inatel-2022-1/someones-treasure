import pygame as pg
from random import choice, randint
from threading import Event
from scripts.camera import Camera
from scripts.constants import *
from scripts.monster import Monster
from scripts.player import Player
from scripts.projectile import Projectile
from scripts.tile import Tile
from scripts.utils import import_folder, import_layout
from scripts.ui import UserInterface


class Level:
    def __init__(self):
        self.visible_sprites = Camera()
        self.solid_block_sprites = pg.sprite.Group()
        self.breakable_block_sprites = pg.sprite.Group()
        self.hole_sprites = pg.sprite.Group()
        self.all_obstacle_sprites = pg.sprite.Group()
        self.projectile_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()
        self.paused = False
        self.__render_map()
        pg.mixer.init()
        pg.mixer.music.load(MUSIC["main_loop"])
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)
        self.game_over_music = pg.mixer.Sound(MUSIC["game_over"])
        self.game_over_music.set_volume(0.5)
        self.game_over = False
        self.death_time = 0
        self.game_over_time = 0
        self.can_continue = False

    def __render_map(self):
        layouts = {
            "hole": import_layout(f"data/map_Holes.csv"),
            "breakable": import_layout(f"data/map_Breakable.csv"),
            "entity": import_layout(f"data/map_Entities.csv"),
            "wall": import_layout(f"data/map_Walls.csv")
        }
        graphics = {
            "breakable": import_folder("images/breakable"),
            "tileset": import_folder("images/tileset")
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != "-1":
                        x = j * TILE_SIZE
                        y = i * TILE_SIZE
                        pos = x, y
                        if style == "hole":
                            groups = [self.hole_sprites,
                                      self.all_obstacle_sprites]
                            Tile(groups, pos, style)
                        if style == "breakable":
                            random_stuff = choice(graphics["breakable"])
                            groups = [self.visible_sprites,
                                      self.breakable_block_sprites,
                                      self.all_obstacle_sprites,
                                      self.attackable_sprites]
                            Tile(groups, pos, style, random_stuff)
                        if style == "entity":
                            if col != "0":
                                groups = [self.visible_sprites,
                                          self.attackable_sprites]
                                obstacles = self.all_obstacle_sprites
                                if col == "1":
                                    monster_name = "slime"
                                    shot_projectile = None
                                elif col == "2":
                                    monster_name = "rat"  # "skeleton"
                                    shot_projectile = self.__shot_projectile
                                elif col == "3":
                                    monster_name = "ghost"
                                    shot_projectile = None
                                    obstacles = None
                                else:
                                    monster_name = "rat"
                                    shot_projectile = self.__shot_projectile
                                Monster(groups, obstacles, pos, monster_name,
                                        self.__damage_player,
                                        self.__add_ammo,
                                        shot_projectile)
                            else:
                                groups = [self.visible_sprites]
                                obstacles = self.all_obstacle_sprites
                                self.player = Player(groups, obstacles, pos,
                                                     self.__shot_projectile)
                                self.ui = UserInterface(self.player)
                        if style == "wall":
                            surface = graphics["tileset"][int(col)]
                            groups = [self.visible_sprites,
                                      self.solid_block_sprites,
                                      self.all_obstacle_sprites]
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
                self.__attack_logic()
        else:
            self.ui.display_game_over()
            if not self.game_over:
                pg.mixer.music.stop()
                self.game_over_music.play()
                self.game_over = True
                self.game_over_time = pg.time.get_ticks()
            current_time = pg.time.get_ticks()
            if current_time - self.game_over_time >= 3000:
                self.can_continue = True

    def pause(self):
        if self.paused:
            pg.mixer.music.unpause()
            self.paused = False
        else:
            pg.mixer.music.pause()
            self.paused = True

    def restart(self):
        if self.can_continue:
            self.__init__()

    def __damage_player(self, amount):
        self.player.take_damage(amount)

    def __shot_projectile(self, entity_state, entity_rect, damage, targets_player=False):
        groups = [self.visible_sprites, self.projectile_sprites]
        obstacles = pg.sprite.Group()
        if not targets_player:
            obstacles.add(self.solid_block_sprites)
        else:
            obstacles.add(self.solid_block_sprites,
                          self.breakable_block_sprites)
        Projectile(groups, obstacles, entity_state, entity_rect,
                   damage, 3, targets_player)

    def __attack_logic(self):
        for projectile in self.projectile_sprites:
            if projectile.targets_player:
                if self.player.rect.colliderect(projectile.hitbox):
                    projectile.kill()
                    self.__damage_player(projectile.damage)
            else:
                for sprite in self.attackable_sprites:
                    if sprite.rect.colliderect(projectile.hitbox):
                        if sprite.style == "monster":
                            sprite.take_damage(projectile.damage)
                        elif sprite.style == "breakable":
                            sprite.kill()
                        projectile.kill()

    def __add_ammo(self, amount=randint(1, 6)):
        self.player.add_ammo(amount)
