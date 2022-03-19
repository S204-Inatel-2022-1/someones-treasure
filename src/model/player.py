import pygame
from src.helper.settings import TILE_SIZE, PLAYER_SPEED


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.walk_buffer = 50
        self.pos = pygame.math.Vector2(x, y) * TILE_SIZE
        self.dirvec = pygame.math.Vector2(0, 0)
        self.last_pos = self.pos
        self.next_pos = self.pos

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.between_tiles = False

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

    def update(self, dt, walls):
        self.get_keys()
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

        if self.pos != self.next_pos:

            delta = self.next_pos - self.pos
            if delta.length() > (self.dirvec * PLAYER_SPEED * dt).length():
                self.pos += self.dirvec * PLAYER_SPEED * dt
            else:
                self.pos = self.next_pos
                self.dirvec = pygame.math.Vector2(0, 0)
                self.between_tiles = False

        self.rect.topleft = self.pos
        if pygame.sprite.spritecollide(self, walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.dirvec = pygame.math.Vector2(0, 0)
            self.between_tiles = False
        self.rect.topleft = self.pos

    def get_keys(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if now - self.last_update > self.walk_buffer:
            self.last_update = now

            new_dir_vec = pygame.math.Vector2(0, 0)
            if self.dirvec.y == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    new_dir_vec = pygame.math.Vector2(-1, 0)
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    new_dir_vec = pygame.math.Vector2(1, 0)
            if self.dirvec.x == 0:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    new_dir_vec = pygame.math.Vector2(0, -1)
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    new_dir_vec = pygame.math.Vector2(0, 1)

            if new_dir_vec != pygame.math.Vector2(0, 0):
                self.dirvec = new_dir_vec
                self.between_tiles = True
                current_index = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
                self.last_pos = pygame.math.Vector2(current_index) * TILE_SIZE
                self.next_pos = self.last_pos + self.dirvec * TILE_SIZE
