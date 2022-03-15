from tkinter import HORIZONTAL
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, position: tuple, groups: pg.sprite.Group,
                 obstacles: pg.sprite.Group):
        super().__init__(groups)
        file = 'assets/img/sprites/player.png'
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pg.math.Vector2()
        self.speed = 5
        self.obstacles = obstacles
        x, y = 0, -26
        self.hitbox = self.rect.inflate(x, y)

    def input(self):
        keys = pg.key.get_pressed()
        # Vertical Axis
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # Horinzontal Axis
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('x')
        self.hitbox.y += self.direction.y * speed
        self.collision('y')
        self.rect.center = self.hitbox.center

    def collision(self, axis):
        if axis == 'x':
            # Horizontal Collisions
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        # Right
                        self.hitbox.right = obstacle.hitbox.left
                    elif self.direction.x < 0:
                        # Left
                        self.hitbox.left = obstacle.hitbox.right
        elif axis == 'y':
            # Vertical Collisions
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        # Down
                        self.hitbox.bottom = obstacle.hitbox.top
                    elif self.direction.y < 0:
                        # Up
                        self.hitbox.top = obstacle.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
