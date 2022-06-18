'''
Contains classes used to control the level's logic, as well as the camera.
'''
from random import choice, randint

from source.constants.settings import TILE_SIZE
from source.level.custom_groups import CustomGroups
from source.sprites.monster import Monster
from source.sprites.player import Player
from source.sprites.projectile import Projectile
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
        self.__render_map()

    def __render_map(self):
        '''
        Renders the map, creating the player, the monsters, the objects, etc.
        '''
        layouts = {
            "hole": import_layout(f"data/{self.lvl_id}/map_Holes.csv"),
            "breakable": import_layout(f"data/{self.lvl_id}/map_Breakable.csv"),
            "entity": import_layout(f"data/{self.lvl_id}/map_Entities.csv"),
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
                        if style == "breakable":
                            self.__create_breakable_tile(pos, style, graphics)
                        if style == "entity":
                            self.__create_entity(int(col), pos)
                        if style == "wall":
                            surface = graphics["tileset"][int(col)]
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
        Tile(groups, pos, style, surface, is_crate)

    def __create_entity(self, num, pos):
        '''
        Creates an entity, such as the player, a monster, etc.
        '''
        if num != 0:
            if num == 1:
                name = "slime"
                damage = self._damage_player
                projectile = None
            elif num == 2:
                name = "rat"
                damage = self._damage_player
                projectile = self._spawn_projectile
                return None
            elif num == 3:
                name = "ghost"
                damage = self._damage_player
                projectile = None
            groups = self.custom_groups.get_groups("entity", name)
            obstacles = self.custom_groups.get_obstacles("entity", name)
            Monster(groups, obstacles, pos, name, damage, projectile)
        else:
            groups = self.custom_groups.get_groups("entity", "player")
            obstacles = self.custom_groups.get_obstacles("entity", "player")
            projectile = self._spawn_projectile
            self.player = Player(groups, obstacles, pos, projectile)
            self.player_ui = PlayerUI(self.player)
        return None

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

    def __projectile_logic(self):
        '''
        Checks if projectiles collide with attackable things.
        '''
        for projectile in self.custom_groups.projectiles_sprites:
            if projectile.targets_player:
                if self.player.rect.colliderect(projectile.hitbox):
                    projectile.kill()
                    self._damage_player(projectile.damage)
            else:
                for sprite in self.custom_groups.attackable_sprites:
                    if sprite.rect.colliderect(projectile.hitbox):
                        sprite.take_damage(projectile.damage)
                        projectile.kill()
            for sprite in self.custom_groups.breakable_sprites:
                if sprite.rect.colliderect(projectile.hitbox):
                    sprite.break_tile()
                    projectile.kill()

    def _spawn_projectile(self, entity_state, entity_rect, power=1, can_hit_player=False):
        '''
        Spawns a projectile relative to the state and "rect" of a given entity.
        '''
        groups = self.custom_groups.get_groups("projectile")
        obstacles = self.custom_groups.get_obstacles("projectile", None)
        Projectile(groups, obstacles, entity_state, entity_rect, damage=power,
                   targets_player=can_hit_player)

    def _damage_player(self, amount=1):
        '''
        Deals a certain amount of damage to the player.
        '''
        self.player.take_damage(amount)

    def _recover_ammo(self, amount=randint(1, 6)):
        '''
        Recovers some of the player's ammunition.
        '''
        self.player.collect_ammo(amount)

    def reset(self):
        '''
        Resets the level. Simple as that.
        '''
        self.custom_groups.reset_all_groups()
        self.__render_map()
