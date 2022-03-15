import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, position: tuple, groups: pg.sprite.Group):
        super().__init__(groups)
        file = 'assets/img/sprites/rock.png'
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        x, y = 0, -10
        self.hitbox = self.rect.inflate(x, y)
