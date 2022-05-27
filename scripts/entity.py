import pygame as pg
from abc import abstractclassmethod
from math import sin
from scripts.constants import *
from scripts.utils import import_folder


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, obstacles, pos, name):
        super().__init__(groups)
        self.style = "monster" if name != "player" else name
        self.obstacles = obstacles
        self.direction = pg.math.Vector2(0, 0)
        if self.style == "player":
            self.__import_animations(name)
        elif self.style == "monster":
            self.__import_animations(f"monsters/{name}")
        self.state = "down"
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
        self.vulnerable = True

    def __import_animations(self, folder_name_path):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }
        for animation in self.animations.keys():
            path = f"images/{folder_name_path}/{animation}"
            self.animations[animation] = import_folder(path)
        self.frame = 0
        self.animation_speed = 0.15

    @abstractclassmethod
    def _validate_state(self):
        pass

    def _move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.__handle_collisions("x")
        self.hitbox.y += self.direction.y * speed
        self.__handle_collisions("y")
        self.rect.center = self.hitbox.center

    def __handle_collisions(self, axis):
        if self.obstacles != None:
            for sprite in self.obstacles:
                if axis == "x":
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                if axis == "y":
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

    def _animate(self):
        animation = self.animations[self.state]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            if "attack" in self.state:
                self._can_attack = False
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.__calculate_wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def __calculate_wave_value(self):
        value = sin(pg.time.get_ticks())
        return 255 if value >= 0 else 0

    def _calculate_relative_vector(self, sprite_rect):
        sprite_vector = pg.math.Vector2(sprite_rect.center)
        self_vector = pg.math.Vector2(self.rect.center)
        vector = sprite_vector - self_vector
        return vector

    def _calculate_relative_distance(self, sprite_rect):
        vector = self._calculate_relative_vector(sprite_rect)
        distance = vector.magnitude()
        return distance

    def _calculate_relative_direction(self, sprite_rect):
        distance = self._calculate_relative_distance(sprite_rect)
        if distance > 0:
            vector = self._calculate_relative_vector(sprite_rect)
            direction = vector.normalize()
        else:
            direction = pg.math.Vector2(0, 0)
        return direction
