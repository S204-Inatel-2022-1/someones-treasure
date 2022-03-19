import pygame
from src.helper.csv_conversion import csv_to_matrix
from src.model.obstacle import Obstacle
from src.model.player import Player


MAP = ["1111111111111111",
       "1..............1",
       "1...........P..1",
       "1..1111........1",
       "1..1..1........1",
       "1..1111........1",
       "1..............1",
       "1........11111.1",
       "1........1...1.1",
       "1........11111.1",
       "1..............1",
       "1111111111111111"]


class Level():
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        # self.map_data = csv_to_matrix('lvl_1')
        for row, tiles in enumerate(MAP):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    obstacle = Obstacle(col, row)
                    self.walls.add(obstacle)
                    self.all_sprites.add(obstacle)
                elif tile == "P":
                    self.player = Player(col, row)
                    self.all_sprites.add(self.player)
