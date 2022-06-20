'''
Contains the CollectableItem class.
'''
import pygame as pg


class AmmoDrop(pg.sprite.Sprite):
    '''
    Class for collectable items.
    '''

    def __init__(self, groups, pos, amount, recover_ammo):
        super().__init__(groups)
        self.image = pg.image.load("images/projectile/drop.png")
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.amount = amount
        self.recover_ammo = recover_ammo

    def collect(self):
        '''
        Collect the item.
        '''
        self.recover_ammo(self.amount)
        self.kill()
