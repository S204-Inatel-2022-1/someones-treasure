import pygame as pg
from source.utils.settings import TILE_SIZE


class Attack(pg.sprite.Sprite):
    def __init__(self, groups, state, entity_rect):
        super().__init__(groups)
        self.direction = state.split("_")[0]
        self._import_graphics()
        self._place_weapon(entity_rect)

    def _import_graphics(self):
        img_path = f"assets/images/weapon/{self.direction}.png"
        self.image = pg.image.load(img_path).convert_alpha()

    def _place_weapon(self, entity_rect):
        if self.direction == "left":
            vector = pg.math.Vector2(0, TILE_SIZE // 4)
            relative_pos = entity_rect.midleft
            self.rect = self.image.get_rect(midright=relative_pos + vector)
        elif self.direction == "right":
            vector = pg.math.Vector2(0, TILE_SIZE // 4)
            relative_pos = entity_rect.midright
            self.rect = self.image.get_rect(midleft=relative_pos + vector)
        elif self.direction == "up":
            vector = pg.math.Vector2(- TILE_SIZE // 4, 0)
            relative_pos = entity_rect.midtop
            self.rect = self.image.get_rect(midbottom=relative_pos + vector)
        elif self.direction == "down":
            vector = pg.math.Vector2(- TILE_SIZE // 4, 0)
            relative_pos = entity_rect.midbottom
            self.rect = self.image.get_rect(midtop=relative_pos + vector)
