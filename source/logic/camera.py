import pygame as pg

from source.constants.settings import TILE_SIZE


class Camera(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2(0, 0)
        self.ground_surf = pg.image.load("images/tile/map.png").convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        self.ground_offset_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, self.ground_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def update_monsters(self, player):
        self.half_width = self.display_surface.get_width() // 2 + TILE_SIZE
        self.half_height = self.display_surface.get_height() // 2 + TILE_SIZE
        monsters = [sprite for sprite in self.sprites()
                    if hasattr(sprite, "custom_update")]
        for monster in monsters:
            distance = monster._calculate_relative_vector(player.rect)
            screen_vector = pg.math.Vector2(self.half_width, self.half_height)
            if abs(distance.x) > abs(screen_vector.x) or \
                    abs(distance.y) > abs(screen_vector.y):
                # print("Monster out of bounds")
                monster.toggle_animations(False)
            else:
                # print("Monster in bounds")
                monster.toggle_animations(True)
            monster.custom_update(player.rect)
