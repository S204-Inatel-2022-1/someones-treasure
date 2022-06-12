from source.ui.ammo_bar import AmmoBar
from source.ui.game_over import GameOverScreen
from source.ui.health_bar import HealthBar
from source.ui.pause import PauseScreen


class UserInterface:
    def __init__(self, player):
        self.hp_bar = HealthBar(player.hp, player.stats["hp"])
        self.ammo_ui = AmmoBar(player.ammo, player.stats["ammo"])
        self.pause_screen = PauseScreen()
        self.game_over_screen = GameOverScreen()

    def display(self, player):
        self.hp_bar.display(player.hp, player.stats["hp"])
        self.ammo_ui.display(player.ammo, player.stats["ammo"])

    def display_pause(self):
        self.pause_screen.display()

    def display_game_over(self):
        self.game_over_screen.display()
