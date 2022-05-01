import pygame as pg
from source.model.attack import Attack
from source.model.bomb import Bomb
from source.model.entity import Entity


class Player(Entity):
    def __init__(self, groups, obstacles, pos):
        super().__init__(groups, obstacles, pos, "player")
        self.walking_speed = 5
        # Attack
        self.attacking = False
        self.attack_cd = 400
        self.attack_update = pg.time.get_ticks()
        # Bomb
        self.bomb_count = 3
        self.active_bomb = False
        self.fuse_time = 1000
        self.bomb_update = pg.time.get_ticks()

    def update(self):
        self._input()
        self._reset_timers()
        self._update_state()
        self._animate()
        self._move(self.walking_speed)

    def _input(self):
        keys = pg.key.get_pressed()
        if not self.attacking:
            self._movement_input(keys)
            # self._attack_input(keys)

    def _reset_timers(self):
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_update >= self.attack_cd:
                self.attacking = False
                self._finish_attack()
        if self.active_bomb:
            if current_time - self.bomb_update >= self.fuse_time:
                self.active_bomb = False
                self.bomb.detonate()

    def _movement_input(self, keys: pg.key.ScancodeWrapper):
        # Vertical
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction.y = -1
            self.state = "up"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction.y = 1
            self.state = "down"
        else:
            self.direction.y = 0
        # Horizontal
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction.x = 1
            self.state = "right"
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction.x = -1
            self.state = "left"
        else:
            self.direction.x = 0

    def _attack_input(self, keys: pg.key.ScancodeWrapper):
        if keys[pg.K_x] or keys[pg.K_z]:
            self.attacking = True
            self.attack_update = pg.time.get_ticks()
            self._initiate_attack()
        if not self.active_bomb:
            if keys[pg.K_SPACE] and self.bomb_count > 0:
                self.active_bomb = True
                self.bomb_count -= 1
                self.bomb_update = pg.time.get_ticks()
                self._place_bomb()

    def _initiate_attack(self):
        self.current_attack = Attack(self.groups(), self.state, self.rect)

    def _finish_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def _place_bomb(self):
        self.bomb = Bomb([self.groups()], self.rect.center)
