import pygame as pg
from source.controller.game import Game
from source.helper.cli import cls


def start():
    cls()
    pg.init()
    game = Game()
    game.run()
