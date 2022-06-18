'''
Contains the base class for all entities.
'''
from math import sin
import pygame as pg

from source.constants.settings import TILE_SIZE
from source.utils.assets import import_folder


class Entity(pg.sprite.Sprite):
    '''
    Base class for entities like the player and monsters.
    '''

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
        self.attacking = False
        self.animated = True
        self.frame = 0
        self.animation_speed = 0.15

    def __import_animations(self, folder_name_path):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }
        for animation in self.animations:
            path = f"images/{folder_name_path}/{animation}"
            self.animations[animation] = import_folder(path)

    def _move(self, speed):
        '''
        Moves the entity.
        '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.__handle_collisions("x")
        self.hitbox.y += self.direction.y * speed
        self.__handle_collisions("y")
        self.rect.center = self.hitbox.center

    def __handle_collisions(self, axis):
        '''
        Handles collisions between the entity and obstacles.
        '''
        if self.obstacles is not None:
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
        '''
        Animates the entity.
        '''
        if self.animated:
            animation = self.animations[self.state]
            self.frame += self.animation_speed
            if self.frame >= len(animation):
                if "attack" in self.state:
                    self.attacking = True
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

    def toggle_animations(self, value):
        '''
        Turns animations ON or OFF.
        '''
        self.animated = value
