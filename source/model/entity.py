import numpy as np
import pygame as pg
from source.utils.asset_management import import_folder
from source.utils.settings import TILE_SIZE


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, obstacles, pos, name):
        super().__init__(groups)
        self.obstacles = obstacles
        self._import_animations(name)
        pos = np.multiply(pos, TILE_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
        self.direction = pg.math.Vector2(0, 0)

    def _import_animations(self, name):
        folder_path = f"assets/images/{name}"
        self.image = pg.image.load(f"{folder_path}/down/0.png").convert_alpha()
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
            "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []
        }
        for animation in self.animations.keys():
            path = folder_path + "/" + animation
            self.animations[animation] = import_folder(path)
        self.animation_speed = 0.15
        self.state = "down"
        self.frame = 0

    def _update_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.state and not "attack" in self.state:
                self.state = self.state + "_idle"
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.state:
                if "idle" in self.state:
                    self.state = self.state.replace("_idle", "_attack")
                else:
                    self.state = self.state + "_attack"
        else:
            if "attack" in self.state:
                self.state = self.state.replace("_attack", "")

    def _animate(self):
        animation = self.animations[self.state]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def _move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self._handle_collisions("x")
        self.hitbox.y += self.direction.y * speed
        self._handle_collisions("y")
        self.rect.center = self.hitbox.center

    def _handle_collisions(self, axis):
        for sprite in self.obstacles:
            if axis == "x":
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
            elif axis == "y":
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
