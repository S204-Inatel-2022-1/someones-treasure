import pygame
import sys
from src.helper.console_control import cls
from src.helper.settings import FPS, TILE_SIZE, WIDTH, HEIGHT
from src.model.game import Game
from src.model.level import Level


def run():
    cls()
    pygame.init()
    game = Game()
    level = Level()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Game closed!')
                pygame.quit()
                sys.exit()
        game.window.fill('white')
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(game.window, 'gray', (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(game.window, 'gray', (0, y), (WIDTH, y))
        dt = game.clock.tick(FPS)
        level.player.update(dt, level.walls)
        level.walls.draw(game.window)
        for sprite in level.all_sprites:
            game.window.blit(sprite.image, sprite.rect)
        pygame.display.flip()
        pygame.display.update()
