'''
Contains the Camera class.
'''
import pygame as pg

from source.utils.calcs import calculate_half_dimensions, calculate_screen_vector
from source.utils.calcs import calculate_relative_vector


class Camera(pg.sprite.Group):
    '''
    This class is used to display the level according to the player's position.
    '''

    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2(0, 0)
        self.ground_surf = pg.image.load("images/tile/map.png").convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        '''
        Draws everything according to player position.
        '''
        half_width, half_height = calculate_half_dimensions()
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
        half_width, half_height = calculate_half_dimensions()
        screen_vector = calculate_screen_vector(half_width, half_height)
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
        Checks if the sprite is visible on the screen.
        '''
        distance = calculate_relative_vector(sprite_rect, player_rect)
        if abs(distance.x) > abs(screen_vector.x) or abs(distance.y) > abs(screen_vector.y):
            return True
        return False
