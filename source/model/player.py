import pygame as pg
from source.controller.settings import TILE_SIZE


class Player(pg.sprite.Sprite):
    def __init__(self, position: tuple, groups: pg.sprite.Group, obstacles: pg.sprite.Group):
        super().__init__(groups)
        self.obstacles = obstacles
        image_path = "assets/images/player/ratinho.png"
        self.image = pg.image.load(image_path).convert_alpha()
        # self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        # self.image.fill("red")
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 2

    def update(self):
        self.input()
        self.move(self.speed)

    def input(self):
        self.direction = pg.math.Vector2(0, 0)
        # if pg.event.type == pg.KEYDOWN:
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.direction.y = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.direction.y = 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.direction.x = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.direction.x = 1

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("x")
        self.hitbox.y += self.direction.y * speed
        self.collision("y")
        self.rect.center = self.hitbox.center

    def collision(self, axis: str):
        for obstacle in self.obstacles:
            if self.hitbox.colliderect(obstacle.hitbox):
                if axis == "x":
                    if self.direction.x > 0:
                        # Moving RIGHT
                        self.hitbox.right = obstacle.hitbox.left
                    elif self.direction.x < 0:
                        # Moving LEFT
                        self.hitbox.left = obstacle.hitbox.right
                if axis == "y":
                    if self.direction.y > 0:
                        # Moving DOWN
                        self.hitbox.bottom = obstacle.hitbox.top
                    elif self.direction.y < 0:
                        # Moving UP
                        self.hitbox.top = obstacle.hitbox.bottom
