'''
Contains classes used to control the level's logic, as well as the camera.
'''
from random import choice, randint
import pygame as pg
from source.constants.paths import SFX

from source.constants.settings import TILE_SIZE
from source.level.custom_groups import CustomGroups
from source.sprites.boss import Boss
from source.sprites.collectable import AmmoDrop
from source.sprites.monster import Monster
from source.sprites.player import Player
from source.sprites.projectile import Projectile
from source.sprites.switch_button import SwitchButton
from source.sprites.tile import Tile
from source.ui import PlayerUI
from source.utils.assets import import_folder, import_layout


class Level:
    '''
    Class used to control all of the level's logic.
    '''

    def __init__(self, lvl_id):
        self.lvl_id = lvl_id
        self.custom_groups = CustomGroups()
        self.player = None
        self.player_ui = None
        self.boss = None
        self.__render_map()
        self.fighting_boss = False

    def __render_map(self):
        '''
        Renders the map, creating the player, the monsters, the objects, etc.
        '''
        layouts = {
            "boss_room": import_layout(f"data/{self.lvl_id}/map_BossRoom.csv"),
            "breakable": import_layout(f"data/{self.lvl_id}/map_BreakableObjects.csv"),
            "hole": import_layout(f"data/{self.lvl_id}/map_Holes.csv"),
            "entity": import_layout(f"data/{self.lvl_id}/map_Entities.csv"),
            "piston": import_layout(f"data/{self.lvl_id}/map_ToggledWalls.csv"),
            "switch": import_layout(f"data/{self.lvl_id}/map_Switches.csv"),
            "wall": import_layout(f"data/{self.lvl_id}/map_Walls.csv")
        }
        graphics = {
            "barrel": import_folder("images/breakable/barrel"),
            "crate": import_folder("images/breakable/crate"),
            "tileset": import_folder("images/tileset")
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != "-1" and col.isdigit():
                        pos = j * TILE_SIZE, i * TILE_SIZE
                        if style == "hole":
                            groups = self.custom_groups.get_groups(style)
                            Tile(groups, pos, style)
                        elif style == "breakable":
                            self.__create_breakable_tile(pos, style, graphics)
                        elif style == "entity":
                            self.__create_entity(int(col), pos)
                        elif style == "wall":
                            surface = graphics["tileset"][int(col)]
                            groups = self.custom_groups.get_groups(style)
                            Tile(groups, pos, style, surface)
                        elif style == "switch":
                            groups = self.custom_groups.get_groups(style)
                            piston = self.custom_groups.get_groups("piston")
                            button = SwitchButton(groups, pos, piston)
                            button.activate_pistons = self._activate_button
                        elif style == "piston":
                            surface = graphics["tileset"][int(col)]
                            groups = self.custom_groups.get_groups(style)
                            Tile(groups, pos, style, surface)
                        elif style == "boss_room":
                            surface = graphics["tileset"][6]
                            groups = self.custom_groups.get_groups(style)
                            Tile(groups, pos, style, surface)

    def __create_breakable_tile(self, pos, style, graphics):
        '''
        Creates a breakable tile, such as a barrel, a crate, etc.
        '''
        if randint(1, 20) < 20:
            surface = choice(graphics["barrel"])
            is_crate = False
        else:
            surface = choice(graphics["crate"])
            is_crate = True
        groups = self.custom_groups.get_groups(style)
        breakable = Tile(groups, pos, style, surface, is_crate)
        breakable.drop_ammo = self._drop_ammo

    def __create_entity(self, num, pos, allow_boss=False):
        '''
        Creates an entity, such as the player, a monster, etc.
        '''
        if num != 0:
            if num == 1:
                name = "slime"
            elif num == 2:
                name = "skeleton"
            elif num == 3:
                name = "ghost"
            elif num == 5:
                name = "abrobra"
            if num <= 3 or allow_boss:
                groups = self.custom_groups.get_groups("entity", name)
                obstacles = self.custom_groups.get_obstacles("entity", name)
                monster = Monster(groups, obstacles, pos, name)
                monster.damage_player = self._damage_player
                monster.shot_projectile = self._spawn_projectile
                monster.drop_ammo = self._drop_ammo
        else:
            groups = self.custom_groups.get_groups("entity", "player")
            obstacles = self.custom_groups.get_obstacles("entity", "player")
            self.player = Player(groups, obstacles, pos)
            self.player.shot_projectile = self._spawn_projectile
            self.player_ui = PlayerUI(self.player)

    def player_alive(self):
        '''
        Checks if the player is still alive.
        '''
        return self.player.health > 0

    def update_view(self):
        '''
        Updates sprites and displays them on screen.
        '''
        self.custom_groups.visible_sprites.custom_draw(self.player)
        self.player_ui.display(self.player)

    def update_logic(self):
        '''
        Updates sprites with more elaborate logic.
        '''
        self.custom_groups.visible_sprites.update()
        self.custom_groups.visible_sprites.update_monsters(self.player)
        self.__projectile_logic()
        self.__check_events()

    def __projectile_logic(self):
        '''
        Checks if projectiles collide with attackable things.
        '''
        for projectile in self.custom_groups.projectiles_sprites:
            if projectile.targets_player:
                if self.player.hitbox.colliderect(projectile.hitbox):
                    projectile.kill()
                    self._damage_player(projectile.damage)
            else:
                for sprite in self.custom_groups.attackable_sprites:
                    if sprite.hitbox.colliderect(projectile.hitbox):
                        sprite.take_damage(projectile.damage)
                        projectile.kill()
            for sprite in self.custom_groups.breakable_sprites:
                if sprite.hitbox.colliderect(projectile.hitbox):
                    sprite.break_tile()
                    projectile.kill()
            for sprite in self.custom_groups.button_sprites:
                if sprite.hitbox.colliderect(projectile.hitbox):
                    sprite.toggle()
                    projectile.kill()
        for collectable in self.custom_groups.collectable_sprites:
            if collectable.hitbox.colliderect(self.player.hitbox):
                collectable.collect()

    def __check_events(self):
        '''
        Checks if the player has pressed a key.
        '''
        for sprite in self.custom_groups.boss_room_sprites:
            if sprite.hitbox.colliderect(self.player.rect):
                self.__trigger_boss_event()

    def _spawn_projectile(self, entity, damage, can_hit_player=False):
        '''
        Spawns a projectile relative to the state and "rect" of a given entity.
        '''
        groups = self.custom_groups.get_groups("projectile")
        obstacles = self.custom_groups.get_obstacles("projectile", None)
        Projectile(groups, obstacles, entity, damage, can_hit_player)

    def _damage_player(self, amount=1):
        '''
        Deals a certain amount of damage to the player.
        '''
        self.player.take_damage(amount)

    def _drop_ammo(self, pos, amount):
        '''
        Drops ammo when the player dies.
        '''
        groups = self.custom_groups.get_groups("collectable")
        AmmoDrop(groups, pos, amount, self._recover_ammo)

    def _recover_ammo(self, amount=1):
        '''
        Recovers some of the player's ammunition.
        '''
        self.player.recover_ammo(amount)

    def reset(self):
        '''
        Resets the level. Simple as that.
        '''
        self.custom_groups.reset_all_groups()
        self.__render_map()

    def _activate_button(self):
        '''
        Activates all buttons.
        '''
        for piston in self.custom_groups.piston_sprites:
            piston.break_tile()

    def __trigger_boss_event(self):
        '''
        Triggers the boss event.
        '''
        for sprite in self.custom_groups.boss_room_sprites:
            sprite.kill()
        layouts = {
            "boss_wall": import_layout(f"data/{self.lvl_id}/map_BossWalls.csv"),
            "entity": import_layout(f"data/{self.lvl_id}/map_Entities.csv")
        }
        graphics = {
            "tileset": import_folder("images/tileset")
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != "-1" and col.isdigit():
                        pos = j * TILE_SIZE, i * TILE_SIZE
                        num = int(col)
                        if style == "boss_wall":
                            surface = graphics["tileset"][num]
                            groups = self.custom_groups.get_groups(style)
                            Tile(groups, pos, style, surface)
                        elif style == "entity":
                            if num == 5:
                                groups = self.custom_groups.get_groups(
                                    style, "abrobra")
                                obstacles = self.custom_groups.get_obstacles(
                                    style, "abrobra")
                                self.boss = Boss(groups, obstacles, pos, self.player,
                                                 self._summon_ghosts)
                                self.boss.damage_player = self._damage_player
                                self.boss.shot_projectile = self._spawn_projectile
                                self.boss.drop_ammo = self._drop_ammo

        self.fighting_boss = True
        sfx = pg.mixer.Sound(SFX["misc"]["break"])
        sfx.set_volume(0.5)
        sfx.play()

    def _summon_ghosts(self, pos, amount):
        '''
        Summons ghosts.
        '''
        for num in range(amount + 1):
            x, y = pos
            if num == 1:
                self.__create_entity(3, (x + TILE_SIZE * 2,
                                         y))
            elif num == 2:
                self.__create_entity(3, (x,
                                         y + TILE_SIZE * 2))
            elif num == 3:
                self.__create_entity(3, (x - TILE_SIZE * 2,
                                         y))
            elif num == 4:
                self.__create_entity(3, (x - TILE_SIZE * 2,
                                         y - TILE_SIZE * 2))

    def boss_alive(self):
        '''
        Checks if the boss is alive.
        '''
        return self.boss.is_alive()

    def destroy_boss_walls(self):
        '''
        Destroys the boss walls.
        '''
        for sprite in self.custom_groups.boss_wall_sprites:
            sprite.break_tile()
