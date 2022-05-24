import pygame as pg
from scripts.entity import Entity
from scripts.constants import *


class Monster(Entity):
    def __init__(self, groups, obstacle_sprites, pos, name):
        super().__init__(groups, obstacle_sprites, pos, name)
        self.stats = STATS[name]
        self.hp = self.stats["hp"]
        self.attacking = False
        self.last_attack = 0
        self.vulnerable = True
        self.last_hit = 0

    def update(self):
        # self.__knockback()
        if not self.attacking:
            self._move(self.stats["speed"])
        self._animate()
        self._reset_timers()
        self.__check_death()

    def custom_update(self, player):
        self._validate_state(player.rect)
        self.__take_action(player.rect)

    def __knockback(self):
        if not self.vulnerable:
            self.direction *= self.knockback_resistance - 10

    def _reset_timers(self):
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.last_attack >= self.stats["attack"]["cooldown"]:
                self.attacking = False
        if not self.vulnerable:
            if current_time - self.last_hit >= self.stats["i_frames"]:
                self.vulnerable = True

    def _validate_state(self, player_rect):
        distance = self._calculate_relative_distance(player_rect)
        if distance > self.stats["range"]["vision_radius"]:
            if not "idle" in self.state:
                if "attack" in self.state:
                    self.state = self.state.replace("attack", "idle")
                else:
                    self.state += "_idle"
                self.attacking = True
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
        if "attack" in self.state:
            self.attack_time = pg.time.get_ticks()
            print("attack")
            # self.damage_player(self.attack_damage, self.attack_type)
            # self.attack_sound.play()
        elif "idle" in self.state:
            self.direction = pg.math.Vector2(0, 0)
        else:
            self.direction = self._calculate_relative_direction(player_rect)
            if self.direction.x > 0:
                self.state = "right"
            elif self.direction.x < 0:
                self.state = "left"

    def __check_death(self):
        if self.hp <= 0:
            self.kill()
            # self.trigger_death_particles(self.rect.center, self.monster_name)
            # self.add_gold(self.gold)
            # self.death_sound.play()

    def take_damage(self, player, attack_type):
        pass
        '''
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self._calculate_relative_direction(player)
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.last_hit = pg.time.get_ticks()
            self.vulnerable = False
        '''
