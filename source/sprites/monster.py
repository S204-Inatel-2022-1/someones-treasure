'''
Contains the Monster class.
'''
import pygame as pg

from source.constants.paths import SFX
from source.constants.stats import STATS
from source.sprites.entity import Entity
from source.utils.calcs import rel_vector, rel_distance, rel_direction


class Monster(Entity):
    '''
    Class used to represent a monster.
    '''

    def __init__(self, groups, obstacle_sprites, pos, name, damage_player, shot_projectile=None):
        super().__init__(groups, obstacle_sprites, pos, name)
        self.stats = STATS[name]
        self.health = self.stats["health"]["max"]
        self.name = name
        self.last_attack = 0
        self.last_hit = 0
        self.can_attack = True
        self.damage_player = damage_player
        # self.drop_ammo = drop_ammo
        self.shot_projectile = shot_projectile

    def update(self):
        '''
        Basic update method.
        '''
        if not self.attacking:
            self.move(self.stats["speed"])
        self._animate()
        self._reset_timers()
        self.__check_death()

    def custom_update(self, player_rect):
        '''
        Custom update method.
        '''
        self._validate_state(player_rect)
        self.__take_action(player_rect)

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

    def _validate_state(self, player_rect):
        '''
        Validates monster state.
        '''
        distance = rel_distance(self.rect, player_rect)
        if distance > self.stats["range"]["vision_radius"]:
            if not "idle" in self.state:
                if "attack" in self.state:
                    self.state = self.state.replace("attack", "idle")
                else:
                    self.state += "_idle"
        else:
            if distance <= self.stats["range"]["aggression_radius"]:
                if not "attack" in self.state:
                    if "iddle" in self.state:
                        self.state = self.state.replace("iddle", "attack")
                    else:
                        self.state += "_attack"
            else:
                if "idle" in self.state:
                    self.state = self.state.replace("_idle", "")
                elif "attack" in self.state:
                    self.state = self.state.replace("_attack", "")

    def __take_action(self, player_rect):
        '''
        Takes action based on the state of the monster.
        '''
        if "attack" in self.state:
            if not self.attacking:
                attack_sfx = pg.mixer.Sound(SFX["attack"][self.name])
                attack_sfx.set_volume(0.5)
                if self.stats["attack"]["type"] == "ranged":
                    vector = rel_vector(self.rect, player_rect)
                    if vector.x // 1 == 0 or vector.y // 1 == 0:
                        self.attacking = True
                        self.last_attack = pg.time.get_ticks()
                        attack_sfx.play()
                        self.shot_projectile(self.state, self.rect, self.stats["attack"]["damage"],
                                             can_hit_player=True)
                else:
                    self.attacking = True
                    self.direction = pg.math.Vector2(0, 0)
                    self.last_attack = pg.time.get_ticks()
                    self.damage_player(self.stats["attack"]["damage"])
                    attack_sfx.play()
            self.direction = pg.math.Vector2(0, 0)
        elif "idle" in self.state:
            self.direction = pg.math.Vector2(0, 0)
        else:
            self.direction = rel_direction(
                self.rect, player_rect)
            if abs(self.direction.x) > abs(self.direction.y):
                if self.direction.x < 0:
                    self.state = "left"
                else:
                    self.state = "right"
            else:
                if self.direction.y < 0:
                    self.state = "up"
                else:
                    self.state = "down"

    def __check_death(self):
        '''
        Checks if the monster is dead.
        '''
        if self.health <= 0:
            self.kill()
            death_sfx = pg.mixer.Sound(SFX["death"][self.name])
            death_sfx.set_volume(0.5)
            death_sfx.play()
            # self.drop_ammo()

    def take_damage(self, amount):
        '''
        The monster takes a certain amount of damage.
        '''
        if self.vulnerable and self.health > 0:
            self.health -= amount
            self.vulnerable = False
            self.last_hit = pg.time.get_ticks()
