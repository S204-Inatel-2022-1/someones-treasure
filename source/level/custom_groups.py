'''
Contains a class with many custom sprite groups.
'''
import pygame as pg

from source.level.camera import Camera


class CustomGroups(pg.sprite.Group):
    '''
    Class containing groups of sprites. Not intended to be used outside of the Level class.
    '''

    def __init__(self):
        self.visible_sprites = Camera()
        self.solid_sprites = pg.sprite.Group()
        self.breakable_sprites = pg.sprite.Group()
        self.holes_sprites = pg.sprite.Group()
        self.obstacles_sprites = pg.sprite.Group()
        self.projectiles_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

    def get_groups(self, style, name=None):
        '''
        Returns which groups a given sprite style belongs to.
        '''
        if style == "hole":
            return [self.holes_sprites, self.obstacles_sprites]
        if style == "breakable":
            return [self.visible_sprites, self.breakable_sprites, self.obstacles_sprites]
        if style == "wall":
            return [self.visible_sprites, self.solid_sprites, self.obstacles_sprites]
        if style == "entity":
            if name == "player":
                return [self.visible_sprites]
            return [self.visible_sprites, self.attackable_sprites]
        return [self.visible_sprites, self.projectiles_sprites]

    def get_obstacles(self, style, name=None):
        '''
        Returns obstacles for a given sprite style.
        '''
        if style == "entity":
            if name == "ghost":
                return None
            return self.obstacles_sprites
        return self.solid_sprites

    def reset_all_groups(self):
        '''
        Kill all groups. Pretty straightforward, huh?
        '''
        all_groups = pg.sprite.Group()
        all_groups.add(self.visible_sprites, self.solid_sprites, self.breakable_sprites,
                       self.holes_sprites, self.obstacles_sprites, self.projectiles_sprites,
                       self.attackable_sprites)
        for sprite in all_groups:
            sprite.kill()
        self.visible_sprites.empty()
        self.solid_sprites.empty()
        self.breakable_sprites.empty()
        self.holes_sprites.empty()
        self.obstacles_sprites.empty()
        self.projectiles_sprites.empty()
        self.attackable_sprites.empty()
