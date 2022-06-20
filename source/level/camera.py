'''
Contains the Camera class.
'''
import pygame as pg

from source.utils.calcs import half_dimensions


class Camera(pg.sprite.Group):
    '''
    This class is used to display stuff according to the player's position.
    '''

    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2(0, 0)
        self.ground_surf = pg.image.load("images/tile/map.png").convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        '''
        Displays everything according to the player's position
        '''
        half_width, half_height = half_dimensions()
        self.offset.x = player.rect.centerx - half_width
        self.offset.y = player.rect.centery - half_height
        ground_offset_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def update_monsters(self, player):
        '''
        Updates the monsters' positions according to the player's position.
        '''
        monsters = [sprite for sprite in self.sprites()
                    if hasattr(sprite, "custom_update")]
        for monster in monsters:
            monster.custom_update(player)
