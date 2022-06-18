'''
Contains the Level class.
'''
from random import choice, randint
import pygame as pg

from source.camera import Camera
from source.constants.settings import TILE_SIZE
from source.sprites.monster import Monster
from source.sprites.player import Player
from source.sprites.projectile import Projectile
from source.sprites.tile import Tile
from source.utils.assets import import_folder, import_layout
from source.ui.player_ui import PlayerUI


class Level:
    '''
    Creates a level, with the player, monsters, and obstacles.
    '''

    def __init__(self):
        # Groups
        self.visible_sprites = Camera()
        self.solid_sprites = pg.sprite.Group()
        self.breakable_sprites = pg.sprite.Group()
        self.holes_sprites = pg.sprite.Group()
        self.players_sprites = pg.sprite.Group()
        self.obstacles_sprites = pg.sprite.Group()
        self.projectiles_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()
        self.entities_sprites = pg.sprite.Group()
        # Map Rendering
        layouts = {
            "hole": import_layout("data/map_Holes.csv"),
            "breakable": import_layout("data/map_Breakable.csv"),
            "entity": import_layout("data/map_Entities.csv"),
            "wall": import_layout("data/map_Walls.csv")
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
                        if style == "hole":
                            Tile([self.holes_sprites, self.obstacles_sprites],
                                 (x, y), style)
                        if style == "breakable":
                            if randint(1, 20) < 20:
                                surface = choice(graphics["barrel"])
                                is_crate = False
                            else:
                                surface = choice(graphics["crate"])
                                is_crate = True
                            Tile([self.visible_sprites, self.breakable_sprites,
                                  self.obstacles_sprites], (x, y), style, surface, is_crate)
                        if style == "entity":
                            if int(col) != 0:
                                if int(col) == 1:
                                    Monster([self.visible_sprites, self.attackable_sprites],
                                            self.obstacles_sprites, (x, y),
                                            "slime", self._damage_player)
                                elif int(col) == 2 and False:
                                    Monster([self.visible_sprites, self.attackable_sprites],
                                            self.obstacles_sprites, (x, y),
                                            "rat", self._damage_player, self._spawn_projectile)
                                elif int(col) == 3:
                                    Monster([self.visible_sprites, self.attackable_sprites],
                                            None, (x, y), "ghost", self._damage_player)
                            else:
                                self.player = Player([self.visible_sprites], self.obstacles_sprites,
                                                     (x, y), self._spawn_projectile)
                                self.player_ui = PlayerUI(self.player)
                        if style == "wall":
                            surface = graphics["tileset"][int(col)]
                            Tile([self.visible_sprites, self.solid_sprites,
                                 self.obstacles_sprites], (x, y), style, surface)

    def player_alive(self):
        '''
        Checks if the player is alive.
        '''
        return self.player.health > 0

    def update_view(self):
        '''
        Updates the sprites and displays them on the screen.
        '''
        self.visible_sprites.custom_draw(self.player)
        self.player_ui.display(self.player)

    def update_logic(self):
        '''
        Updastes sprites with more elaborate logic.
        '''
        self.visible_sprites.update()
        self.visible_sprites.update_monsters(self.player)
        self.__projectile_logic()

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

    def _spawn_projectile(self, entity_state, entity_rect, power=1, can_hit_player=False):
        '''
        Spawns a projectile.
        '''
        Projectile([self.visible_sprites, self.projectiles_sprites], self.solid_sprites,
                   entity_state, entity_rect, damage=power, targets_player=can_hit_player)

    def _damage_player(self, amount=1):
        '''
        Deals damage to the player.
        '''
        self.player.take_damage(amount)

    def _recover_ammo(self, amount=randint(1, 6)):
        '''
        Recovers player's ammo.
        '''
        self.player.collect_ammo(amount)
