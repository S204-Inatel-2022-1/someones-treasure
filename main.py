'''
Main file for the program.
'''
import sys
import pygame as pg

from source.constants.settings import RESOLUTION, FPS
from source.constants.paths import ICON, MUSIC
from source.level import Level
from source.utils.cli import clear
from source.ui.debugging import display_info
from source.ui.screens import GameOverScreen, PauseScreen


class Game:
    '''
    This is the main class of the game. It controls most of the game flow.
    '''

    def __init__(self):
        pg.init()
        # Window
        self.screen = pg.display.set_mode(RESOLUTION, pg.RESIZABLE)
        pg.display.set_caption("Someone's Treasure")
        pg.display.set_icon(pg.image.load(ICON).convert_alpha())
        # Game State
        self.paused = False
        self.game_over = False
        self.can_continue = False
        self.death_time = 0
        # Clock
        self.clock = pg.time.Clock()
        # Level
        self.level = Level()
        # UI
        self.game_over_screen = GameOverScreen()
        self.pause_screen = PauseScreen()
        # Music
        pg.mixer.init()
        pg.mixer.music.load(MUSIC["main_loop"])
        pg.mixer.music.set_volume(0.2)
        self.game_over_music = pg.mixer.Sound(MUSIC["game_over"])
        self.game_over_music.set_volume(0.3)

    def run(self):
        '''
        Runs the game.
        '''
        self.__initialize()
        while True:
            self.clock.tick(FPS)
            self.screen.fill("black")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.close()
                    if event.key == pg.K_RETURN:
                        if not self.game_over:
                            self.__toggle_pause()
                        elif self.can_continue:
                            self.__initialize()
            if self.level.player_alive():
                self.level.update_view()
                if not self.paused:
                    self.level.update_logic()
                else:
                    self.pause_screen.display()
            else:
                if not self.game_over:
                    pg.mixer.music.stop()
                    self.game_over_music.play()
                    self.death_time = pg.time.get_ticks()
                self.game_over = True
                self.game_over_screen.display()
                time_difference = pg.time.get_ticks() - self.death_time
                if time_difference > 5500 and not self.can_continue:
                    self.can_continue = True
                    # show a message or something
            display_info(int(self.clock.get_fps()))
            pg.display.update()

    def close(self):
        '''
        Closes the game.
        '''
        print("GAME OVER!\n")
        pg.quit()
        sys.exit()

    def __toggle_pause(self):
        '''
        Pauses or unpauses the game.
        '''
        self.paused = not self.paused
        if pg.mixer.music.get_busy():
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()

    def __initialize(self):
        '''
        Initializes the game. Usually called when the game is restarted.
        '''
        self.level = Level()
        pg.mixer.music.play(-1)
        self.can_continue = False
        self.paused = False
        self.game_over = False


if __name__ == "__main__":
    clear()
    game = Game()
    game.run()
