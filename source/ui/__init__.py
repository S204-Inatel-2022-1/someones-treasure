'''
Contains modules for Player UI, Game Over and Pause screens.
'''
import pygame as pg

from source.constants.paths import FONT
from source.constants.settings import TITLE
from source.ui.components import HealthBar, AmmoBar


class PlayerUI:
    '''
    Class to display the player's health and ammo.
    '''

    def __init__(self, player):
        self.hp_bar = HealthBar(player.health,
                                player.stats["health"]["max"])
        self.ammo_ui = AmmoBar(player.ammo,
                               player.stats["ammo"]["max"])

    def display(self, player):
        '''
        Displays the player's health and ammo.
        '''
        self.hp_bar.display(player.health,
                            player.stats["health"]["max"])
        self.ammo_ui.display(player.ammo,
                             player.stats["ammo"]["max"])


class GameOverScreen:
    '''
    Class used to display the game over screen.
    '''

    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.image = pg.image.load("images/game-over/very_sad_rat.png")

    def display(self):
        '''
        Displays a message to the player indicating that their character has died.
        '''
        font = pg.font.Font(FONT, 64)
        text = font.render("GAME OVER", False, "red")
        width, height = self.display_surface.get_width(), self.display_surface.get_height()
        image_rect = self.image.get_rect(center=(width // 2, height // 2))
        text_rect = text.get_rect(center=(width // 2, height * 0.75))
        self.display_surface.blit(self.image, image_rect)
        self.display_surface.blit(text, text_rect)

    def show_continue_msg(self):
        '''
        Displays a message to the player, prompting them to press a button to continue playing.
        '''
        font = pg.font.Font(FONT, 32)
        text = font.render("Press Enter to continue...", False, "red")
        width, height = self.display_surface.get_width(), self.display_surface.get_height()
        text_rect = text.get_rect(center=(width // 2, height * 0.85))
        self.display_surface.blit(text, text_rect)


class PauseScreen:
    '''
    Class to display the pause screen.
    '''

    def __init__(self):
        self.display_surface = pg.display.get_surface()
        font = pg.font.Font(FONT, 36)
        self.text = font.render("PAUSED", False, "white")

    def display(self):
        '''
        Display a message to the user indicating that the game is paused.
        '''
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()
        text_rect = self.text.get_rect(center=(width // 2, height // 2))
        self.display_surface.blit(self.text, text_rect)


class StartMenu:
    '''
    Class to display the start menu.
    '''

    def __init__(self):
        self.display_surface = pg.display.get_surface()
        title_font = pg.font.Font(FONT, 64)
        button_font = pg.font.Font(FONT, 36)
        self.title = title_font.render(TITLE, False, "white")
        self.button_1 = button_font.render("Play", False, "white", None)
        self.button_2 = button_font.render("Quit", False, "white", None)
        self.title_rect = None
        self.button_1_rect = None
        self.button_2_rect = None

    def display(self):
        '''
        Display a message to the user indicating that the game is paused.
        '''
        width, height = self.display_surface.get_width(), self.display_surface.get_height()
        self.title_rect = self.title.get_rect(center=(width // 2,
                                                      height * 0.25))
        self.button_1_rect = self.button_1.get_rect(center=(width // 2,
                                                            height * 0.65))
        self.button_2_rect = self.button_2.get_rect(center=(width // 2,
                                                            height * 0.85))
        self.display_surface.blit(self.title, self.title_rect)
        self.display_surface.blit(self.button_1, self.button_1_rect)
        self.display_surface.blit(self.button_2, self.button_2_rect)

    def button_pressed(self, mouse_pos):
        '''
        Returns 1 if the Start button is pressed or -1 if the Quit button is pressed.
        Returns None if neither button is pressed.
        For it to be pressed, the mouse must be above it and press it.
        '''
        if self.button_1_rect.collidepoint(mouse_pos):
            return 1
        if self.button_2_rect.collidepoint(mouse_pos):
            return -1
        return None
