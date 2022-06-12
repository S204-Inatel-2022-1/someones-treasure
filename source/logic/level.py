import pygame as pg
from random import choice, randint
from source.constants.paths import *
from source.constants.stats import *
from source.logic.camera import Camera
from source.logic.utils import import_folder, import_layout
from source.sprites.monster import Monster
from source.sprites.player import Player
from source.sprites.projectile import Projectile
from source.sprites.tile import Tile
from source.ui.ui import UserInterface


class Level:
    def __init__(self):
        self.visible_sprites = Camera()
        self.solid_sprites = pg.sprite.Group()
        self.breakable_sprites = pg.sprite.Group()
        self.holes_sprites = pg.sprite.Group()
        self.players_sprites = pg.sprite.Group()
        self.obstacles_sprites = pg.sprite.Group()
        self.projectiles_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()
        self.__render_map()
        pg.mixer.init()
        pg.mixer.music.load(MUSIC["main_loop"])
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)
        self.paused = False
        self.game_over_music = pg.mixer.Sound(MUSIC["game_over"])
        self.game_over_music.set_volume(0.3)
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
            "barrel": import_folder("images/breakable/barrel"),
            "crate": import_folder("images/breakable/crate"),
            "tileset": import_folder("images/tileset")
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if int(col) != -1:
                        x = j * TILE_SIZE
                        y = i * TILE_SIZE
                        pos = x, y
                        if style == "hole":
                            Tile([self.holes_sprites, self.obstacles_sprites],
                                 pos, style)
                        if style == "breakable":
                            if randint(1, 20) < 20:
                                surface = choice(graphics["barrel"])
                                is_crate = False
                            else:
                                surface = choice(graphics["crate"])
                                is_crate = True
                            Tile([self.visible_sprites, self.breakable_sprites,
                                 self.obstacles_sprites], pos, style, surface, is_crate)
                        if style == "entity":
                            if int(col) != 0:
                                if int(col) == 1:
                                    Monster([self.visible_sprites, self.attackable_sprites],
                                            self.obstacles_sprites, pos, "slime", self._damage_player)
                                elif int(col) == 2:
                                    Monster([self.visible_sprites, self.attackable_sprites], self.obstacles_sprites,
                                            pos, "rat", self._damage_player, self._spawn_projectile)
                                elif int(col) == 3:
                                    Monster([self.visible_sprites, self.attackable_sprites],
                                            None, pos, "ghost", self._damage_player)
                            else:
                                self.player = Player([self.visible_sprites], self.obstacles_sprites, pos,
                                                     self._spawn_projectile)
                                self.ui = UserInterface(self.player)
                        if style == "wall":
                            surface = graphics["tileset"][int(col)]
                            Tile([self.visible_sprites, self.solid_sprites,
                                 self.obstacles_sprites], pos, style, surface)

    def run(self):
        if self.player.hp > 0:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            if self.paused:
                self.ui.display_pause()
            else:
                self.visible_sprites.update()
                self.visible_sprites.update_monsters(self.player)
                self.__projectile_logic()
        else:
            if not self.game_over:
                pg.mixer.music.stop()
                self.game_over_music.play()
                self.game_over = True
                self.game_over_time = pg.time.get_ticks()
            self.ui.display_game_over()
            current_time = pg.time.get_ticks()
            if current_time - self.game_over_time >= 3000:
                self.can_continue = True

    def __projectile_logic(self):
        for projectile in self.projectiles_sprites:
            if projectile.targets_player:
                if self.player.rect.colliderect(projectile.hitbox):
                    projectile.kill()
                    self._damage_player(projectile.damage)
            else:
                for sprite in self.attackable_sprites:
                    if sprite.rect.colliderect(projectile.hitbox):
                        sprite.take_damage(projectile.damage)
                        projectile.kill()
            for sprite in self.breakable_sprites:
                if sprite.rect.colliderect(projectile.hitbox):
                    sprite.break_tile()
                    projectile.kill()

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

    def _spawn_projectile(self, entity_state, entity_rect, power=1, can_hit_player=False):
        Projectile([self.visible_sprites, self.projectiles_sprites], self.solid_sprites,
                   entity_state, entity_rect, damage=power, targets_player=can_hit_player)

    def _damage_player(self, amount=1):
        self.player.take_damage(amount)

    def _recover_ammo(self, amount=randint(1, 6)):
        self.player.collect_ammo(amount)
