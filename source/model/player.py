import pygame as pg
from source.helper.settings import TILE_SIZE
from source.helper.import_assets import get_folder


class Player(pg.sprite.Sprite):
    def __init__(self, position: tuple, sprites: list, obstacles: pg.sprite.Group):
        super().__init__(sprites)
        self.obstacles = obstacles
        img_path = "assets/images/player/down/0.png"
        self.image = pg.image.load(img_path).convert_alpha()
        position = position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, - TILE_SIZE // 4)
        self.__import_animations__()
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 5
        self.attacking = False
        self.cooldown = 400
        self.last_update = pg.time.get_ticks()
        self.state = "down"
        self.frame = 0
        self.animation_speed = 0.5

    def __import_animations__(self):
        folder = "assets/images/player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }
        for animation in self.animations.keys():
            path = folder + animation
            self.animations[animation] = get_folder(path)

    def update(self):
        self.__input_controls__()
        self.__set_state__()
        self.__animate__()
        self.__move__(self.speed)

    def __input_controls__(self):
        keys = pg.key.get_pressed()
        if not self.attacking:
            self.__movement_input__(keys)
            self.__attack_input__(keys)

    def __movement_input__(self, keys: pg.key.ScancodeWrapper):
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction.y = -1
            self.state = "up"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction.y = 1
            self.state = "down"
        else:
            self.direction.y = 0
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction.x = 1
            self.state = "right"
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction.x = -1
            self.state = "left"
        else:
            self.direction.x = 0

    def __attack_input__(self, keys: pg.key.ScancodeWrapper):
        pass

    def __set_state__(self):
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

    def __animate__(self):
        animation = self.animations[self.state]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def __move__(self, speed: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.__threat_collisions__("x")
        self.hitbox.y += self.direction.y * speed
        self.__threat_collisions__("y")
        self.rect.center = self.hitbox.center

    def __threat_collisions__(self, axis: str):
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
