'''
Contains the Player class.
'''
import pygame as pg

from source.constants.paths import SFX
from source.constants.stats import STATS
from source.sprites.entity import Entity


class Player(Entity):
    '''
    Class used to represent the player.
    '''

    def __init__(self, groups, obstacles, pos):
        super().__init__(groups, obstacles, pos, "player")
        self.stats = STATS["player"]
        self.health = self.stats["health"]["max"]
        self.ammo = self.stats["ammo"]["max"]
        self.last_attack = 0
        self.last_hit = 0
        self.speed = self.stats["speed"]
        self.damage = self.stats["attack"]["damage"]

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

    def update(self):
        '''
        Basic update method.
        '''
        self.__input()
        self._reset_timers()
        self._validate_state()
        self._animate()
        self.move(self.speed)
        self.__check_death()

    def __input(self):
        '''
        General input method.
        '''
        if not self.attacking:
            keys = pg.key.get_pressed()
            self.__movement_input(keys)
            self.__attack_input(keys)

    def __movement_input(self, keys):
        '''
        Gets the player's movement input.
        '''
        # Vertical
        if keys[pg.K_w]:
            self.direction.y = -1
            self.state = "up"
        elif keys[pg.K_s]:
            self.direction.y = 1
            self.state = "down"
        else:
            self.direction.y = 0
        # Horizontal
        if keys[pg.K_d]:
            self.direction.x = 1
            self.state = "right"
        elif keys[pg.K_a]:
            self.direction.x = -1
            self.state = "left"
        else:
            self.direction.x = 0

    def __attack_input(self, keys):
        '''
        Gets the player's attack input.
        '''
        attack = False
        if keys[pg.K_UP]:
            attack = True
            self.state = "up"
        elif keys[pg.K_DOWN]:
            attack = True
            self.state = "down"
        elif keys[pg.K_LEFT]:
            attack = True
            self.state = "left"
        elif keys[pg.K_RIGHT]:
            attack = True
            self.state = "right"
        if attack:
            if self.ammo > 0:
                self.attacking = True
                self.last_attack = pg.time.get_ticks()
                self.animation_speed *= 2
                self.__shot()
            else:
                # Something like this
                # sfx = pg.mixer.Sound("sounds/empty_gun.wav")
                # sfx.set_volume(0.5)
                # sfx.play()
                pass

    def __shot(self):
        '''
        Creates a new projectile and fires it.
        '''
        self.ammo -= 1
        damage = self.damage
        self.__shot_projectile(self, damage)

    def _reset_timers(self):
        '''
        Resets cooldowns.
        '''
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.last_attack >= self.stats["attack"]["cooldown"]:
                self.attacking = False
                self.animation_speed /= 2
                # self.__finish_attack()
        if not self.vulnerable:
            if current_time - self.last_hit >= self.stats["i_frames"]:
                self.vulnerable = True

    def __check_death(self):
        if self.health <= 0:
            self.kill()
            death_sfx = pg.mixer.Sound(SFX["death"]["player"])
            death_sfx.play()

    def take_damage(self, amount):
        '''
        The player takes a certain amount of damage.
        If they are not vulnerable, the damage is ignored.
        '''
        if self.vulnerable and self.health > 0:
            self.health -= amount
            self.vulnerable = False
            self.last_hit = pg.time.get_ticks()

    def recover_ammo(self, amount):
        '''
        Recovers a certain ammount of the player's ammunition.
        '''
        if self.ammo + amount <= self.stats["ammo"]["max"]:
            self.ammo += amount
        else:
            self.ammo = self.stats["ammo"]["max"]
