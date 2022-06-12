import pygame as pg
from source.constants.paths import *
from source.constants.stats import *
from source.sprites.entity import Entity
from source.sprites.projectile import Projectile


class Monster(Entity):
    def __init__(self, groups, obstacle_sprites, pos, name, damage_player, shot_projectile=None):
        super().__init__(groups, obstacle_sprites, pos, name)
        self.stats = STATS[name]
        self.hp = self.stats["hp"]
        self.attacking = False
        self.last_attack = 0
        self.last_hit = 0
        self.damage_player = damage_player
        # self.drop_ammo = drop_ammo
        self.shot_projectile = shot_projectile
        self.attack_sfx = pg.mixer.Sound(SFX["attack"][name])
        self.attack_sfx.set_volume(0.5)
        self.death_sfx = pg.mixer.Sound(SFX["death"][name])
        self.death_sfx.set_volume(0.5)

    def update(self):
        # self.__knockback()
        if not self.attacking:
            self._move(self.stats["speed"])
        self._animate()
        self._reset_timers()
        self.__check_death()

    def custom_update(self, player_rect):
        self._validate_state(player_rect)
        self.__take_action(player_rect)

    def __knockback(self):
        if not self.vulnerable:
            self.direction *= self.knockback_resistance - 64

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
        if "attack" in self.state and not self.attacking:
            if self.stats["attack"]["type"] == "ranged":
                relative_vector = self._calculate_relative_vector(player_rect)
                if relative_vector.x // 1 == 0 or relative_vector.y // 1 == 0 or True:
                    self.attacking = True
                    self.last_attack = pg.time.get_ticks()
                    self.attack_sfx.play()
                    self.shot_projectile(self.state, self.rect, self.stats["attack"]["damage"],
                                         can_hit_player=True)
            else:
                self.attacking = True
                self.direction = pg.math.Vector2(0, 0)
                self.last_attack = pg.time.get_ticks()
                self.damage_player(self.stats["attack"]["damage"])
                self.attack_sfx.play()
            self.direction = pg.math.Vector2(0, 0)
        elif "idle" in self.state:
            self.direction = pg.math.Vector2(0, 0)
        else:
            self.direction = self._calculate_relative_direction(player_rect)
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
        if self.hp <= 0:
            self.kill()
            self.death_sfx.play()
            # self.drop_ammo()

    def take_damage(self, amount):
        if self.vulnerable and self.hp > 0:
            self.hp -= amount
            self.vulnerable = False
            self.last_hit = pg.time.get_ticks()
