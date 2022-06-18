'''
Contains the PlayerUI class.
'''
from source.ui.components import HealthBar, AmmoBar


class PlayerUI:
    '''
    Class to display the player's health and ammo.
    '''

    def __init__(self, player):
        self.hp_bar = HealthBar(player.health, player.stats["hp"])
        self.ammo_ui = AmmoBar(player.ammo, player.stats["ammo"])

    def display(self, player):
        '''
        Displays the player's health and ammo.
        '''
        self.hp_bar.display(player.health, player.stats["hp"])
        self.ammo_ui.display(player.ammo, player.stats["ammo"])
