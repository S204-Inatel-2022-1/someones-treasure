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
        self.obstacles = obstacles
        self.direction = pg.math.Vector2(0, 0)
        style = "monster" if name != "player" else name
        self.animations = self.__import_animations(style, name)
        self.state = "down_idle"
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
        self.vulnerable = True
        self.attacking = False
        self.animated = True
        self.frame = 0
        self.animation_speed = 0.15

    def __import_animations(self, style, name):
        '''
        Imports the animations of the entity.
        '''
        if style == "player":
            folder_name_path = "player/"
        elif style == "monster":
            folder_name_path = f"monsters/{name}"
        animations = animation_list = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }
        for animation in animation_list:
            path = f"images/{folder_name_path}/{animation}"
            animations[animation] = import_folder(path)
        return animations

    def move(self, speed):
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
        '''
        Calculates the alpha value of the entity.
        '''
        value = sin(pg.time.get_ticks())
        return 255 if value >= 0 else 0

    def toggle_animations(self, value):
        '''
        Enables or disables animations.
        '''
        self.animated = value

    def _validate_state(self):
        '''
        Validates player state.
        '''
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.state and "attack" not in self.state:
                self.state += "_idle"
        if self.attacking:
            self.direction = pg.Vector2(0, 0)
            if "attack" not in self.state:
                if "idle" in self.state:
                    self.state = self.state.replace("_idle", "_attack")
                else:
                    self.state += "_attack"
        else:
            if "attack" in self.state:
                self.state = self.state.replace("_attack", "")
