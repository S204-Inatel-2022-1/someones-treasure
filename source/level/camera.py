'''
Contains the Camera class.
'''
import pygame as pg

from source.constants.settings import TILE_SIZE
from source.utils.calcs import half_dimensions, rel_vector


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
        half_width, half_height = half_dimensions()
        screen_vector = self.__calc_screen_vector(half_width, half_height,
                                                  TILE_SIZE)
        monsters = [sprite for sprite in self.sprites()
                    if hasattr(sprite, "custom_update")]
        for monster in monsters:
            if self.__sprite_is_visible(monster.rect, player.rect, screen_vector):
                monster.toggle_animations(False)
            else:
                monster.toggle_animations(True)
                monster.custom_update(player.rect)

    def __sprite_is_visible(self, sprite_rect, player_rect, screen_vector):
        '''
        Checks if a sprite is visible on the screen.
        '''
        distance = rel_vector(sprite_rect, player_rect)
        if abs(distance.x) > abs(screen_vector.x) or abs(distance.y) > abs(screen_vector.y):
            return True
        return False

    def __calc_screen_vector(self, half_width, half_height, scalar=0):
        '''
        Calculates a vector representing the screen plus a scalar.
        '''
        return pg.math.Vector2(half_width + scalar, half_height + scalar)
