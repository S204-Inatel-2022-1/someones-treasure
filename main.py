from source.controller.game import Game
from source.utils.cli_helper import cls


if __name__ == '__main__':
    cls()
    game = Game()
    game.run()
