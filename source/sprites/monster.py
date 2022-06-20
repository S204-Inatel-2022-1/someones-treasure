'''
Contains the Monster class.
'''
from random import randint
import pygame as pg

from source.constants.paths import SFX
# from source.constants.settings import TILE_SIZE
from source.constants.stats import STATS
from source.sprites.entity import Entity
from source.utils.calcs import rel_direction, rel_distance


class Monster(Entity):
    '''
    Class used to represent a monster.
    '''

    def __init__(self, groups, obstacle_sprites, pos, name):
        super().__init__(groups, obstacle_sprites, pos, name)
        self.stats = STATS[name]
        self.health = self.stats["health"]["max"]
        self.name = name
        self.last_attack = 0
        self.last_hit = 0
        self.speed = self.stats["speed"]
        self.damage = self.stats["attack"]["damage"]

    def update(self):
        '''
        Basic update method.
        '''
        self._animate()
        self._reset_timers()
        self.__check_death()

    def custom_update(self, player):
        '''
        Custom update method.
        '''
        self._validate_state()
        self.__take_action(player.rect)

    def _reset_timers(self):
        '''
        Resets cooldowns.
        '''
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.last_attack >= self.stats["attack"]["cooldown"]:
                self.attacking = False
        if not self.vulnerable:
            if current_time - self.last_hit >= self.stats["i_frames"]:
                self.vulnerable = True

    def __take_action(self, player_rect):
        '''
        Takes action based on the position of the player.
        '''
        distance = rel_distance(self.rect, player_rect)
        if not self.attacking:
            if distance <= self.stats["range"]["aggression_radius"]:
                damage = self.damage
                if self.stats["attack"]["type"] != "ranged":
                    self.__damage_player(damage)
                else:
                    self.__shot_projectile(self, damage, True)
                self.attacking = True
                self.last_attack = pg.time.get_ticks()
                sfx = pg.mixer.Sound(SFX["attack"][self.name])
                sfx.set_volume(0.5)
                sfx.play()
            elif distance <= self.stats["range"]["vision_radius"]:
                self.direction = rel_direction(self.rect, player_rect)
                direction = rel_direction(self.rect, player_rect)
                if abs(direction.x) > abs(direction.y):
                    if direction.x > 0:
                        self.state = "right"
                    elif direction.x < 0:
                        self.state = "left"
                else:
                    if direction.y > 0:
                        self.state = "down"
                    elif direction.y < 0:
                        self.state = "up"
                self.move(self.speed)
            else:
                self.direction = pg.math.Vector2(0, 0)
        else:
            self.direction = pg.math.Vector2(0, 0)

    def __check_death(self):
        '''
        Checks if the monster is dead.
        '''
        if self.health <= 0:
            self.kill()
            death_sfx = pg.mixer.Sound(SFX["death"][self.name])
            death_sfx.set_volume(0.5)
            death_sfx.play()
            pos = self.rect.center
            chance = randint(1, 100)
            if chance <= 25:
                qty = randint(1, 3)
                self._drop_ammo(pos, qty)

    def take_damage(self, amount):
        '''
        The monster takes a certain amount of damage.
        '''
        if self.vulnerable and self.health > 0:
            self.health -= amount
            self.vulnerable = False
            self.last_hit = pg.time.get_ticks()
            sfx = pg.mixer.Sound(SFX["misc"]["hit"])
            sfx.set_volume(0.3)
            sfx.play()

    @property
    def damage_player(self):
        '''
        Getter.
        '''
        return self.__damage_player

    @damage_player.setter
    def damage_player(self, function):
        '''
        Setter.
        '''
        self.__damage_player = function

    @property
    def shot_projectile(self):
        '''
        Getter.
        '''
        return self.__shot_projectile

    @shot_projectile.setter
    def shot_projectile(self, function):
        '''
        Setter.
        '''
        self.__shot_projectile = function

    @property
    def drop_ammo(self):
        '''
        Getter.
        '''
        return self._drop_ammo

    @drop_ammo.setter
    def drop_ammo(self, function):
        '''
        Setter.
        '''
        self._drop_ammo = function
