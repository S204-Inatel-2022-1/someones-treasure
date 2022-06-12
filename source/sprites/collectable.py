import pygame as pg


class Collectable(pg.sprite.Sprite):
    def __init__(self, groups, pos, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
