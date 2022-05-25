import pygame as pg
from scripts.constants import *


class Projectile(pg.sprite.Sprite):
    def __init__(self, groups, obstacles, entity_state, entity_rect, speed=3):
        super().__init__(groups)
        self.obstacles = obstacles
        self.speed = speed
        # State
        state = entity_state.split("_")[0]
        # Image
        self.image = pg.image.load(f"images/projectile/{state}.png")
        self.image = self.image.convert_alpha()
        # Sound
        sfx = pg.mixer.Sound(SFX["attack"]["player"])
        sfx.set_volume(0.2)
        sfx.play()
        # Placement
        self.__placement(entity_rect, state)

    def __placement(self, entity_rect, state):
        if state == "left":
            vector = pg.math.Vector2(0, TILE_SIZE // 4)
            relative_pos = entity_rect.midleft
            self.rect = self.image.get_rect(midright=relative_pos + vector)
            self.__direction = pg.math.Vector2(- self.speed, 0)
        elif state == "right":
            vector = pg.math.Vector2(0, TILE_SIZE // 4)
            relative_pos = entity_rect.midright
            self.rect = self.image.get_rect(midleft=relative_pos + vector)
            self.__direction = pg.math.Vector2(self.speed, 0)
        elif state == "up":
            vector = pg.math.Vector2(TILE_SIZE // 4, 0)
            relative_pos = entity_rect.midtop
            self.rect = self.image.get_rect(midbottom=relative_pos + vector)
            self.__direction = pg.math.Vector2(0, - self.speed)
        elif state == "down":
            vector = pg.math.Vector2(- TILE_SIZE // 4, 0)
            relative_pos = entity_rect.midbottom
            self.rect = self.image.get_rect(midtop=relative_pos + vector)
            self.__direction = pg.math.Vector2(0, self.speed)
        self.hitbox = self.rect

    def update(self):
        self.__move(self.speed)
        self.__handle_collisions()

    def __move(self, speed):
        self.hitbox.x += self.__direction.x * speed
        self.hitbox.y += self.__direction.y * speed
        self.__handle_collisions()
        self.rect.center = self.hitbox.center

    def __handle_collisions(self):
        for sprite in self.obstacles:
            if sprite.hitbox.colliderect(self.hitbox):
                self.kill()
