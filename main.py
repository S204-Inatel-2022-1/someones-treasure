'''
Main program file.
'''
import sys
import pygame as pg

from source.constants.settings import RESOLUTION, TITLE, FPS
from source.constants.paths import ICON, MUSIC
from source.level import Level
from source.utils.cli import clear
from source.ui import GameOverScreen, PauseScreen, StartMenu
from source.ui.debugging import display_info


class Game:
    '''
    This is the main class in the game. It controls most of the game flow.
    '''

    def __init__(self):
        pg.init()
        # Window
        self.window = pg.display.set_mode(RESOLUTION, pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load(ICON).convert_alpha())
        # Level
        self.level = None
        # Game State
        self.game_state = "start"
        self.death_time = 0
        # Clock
        self.clock = pg.time.Clock()
        # UI
        self.game_over_screen = GameOverScreen()
        self.pause_screen = PauseScreen()
        self.start_menu = StartMenu()
        # Mixer
        pg.mixer.init()
        pg.mixer.music.load(MUSIC["main_loop"])
        pg.mixer.music.set_volume(0.2)

    def run(self):
        '''
        Main game loop.
        '''
        while True:
            self.clock.tick(FPS)
            self.window.fill("black")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                if self.game_state != "start":
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.close()
                        elif event.key == pg.K_RETURN:
                            self.__start_button()
                elif event.type == pg.MOUSEBUTTONUP:
                    value = self.start_menu.button_pressed(pg.mouse.get_pos())
                    if value == 1:
                        self.level = Level(0)
                        pg.mixer.music.play(-1)
                        self.game_state = "running"
                    elif value == -1:
                        self.close()
            if self.game_state != "start":
                if self.level.player_alive():
                    self.__update_level()
                else:
                    self.__show_game_over()
            else:
                self.start_menu.display()
            display_info(int(self.clock.get_fps()))
            pg.display.update()

    def close(self):
        '''
        Closes the game.
        '''
        print("GAME OVER!\n")
        pg.quit()
        sys.exit()

    def __update_level(self):
        '''
        Updates the level.
        '''
        self.level.update_view()
        if self.game_state != "pause":
            self.level.update_logic()
        else:
            self.pause_screen.display()

    def __show_game_over(self):
        '''
        Shows the game over screen.
        '''
        if not self.game_state in ["game over", "continue"]:
            pg.mixer.music.stop()
            game_over_music = pg.mixer.Sound(MUSIC["game_over"])
            game_over_music.set_volume(0.3)
            game_over_music.play()
            self.death_time = pg.time.get_ticks()
        self.game_state = "game over"
        self.game_over_screen.display()
        time_difference = pg.time.get_ticks() - self.death_time
        if time_difference > 5500 and self.game_state != "continue":
            self.game_state = "continue"
            self.game_over_screen.show_continue_msg()

    def __start_button(self):
        '''
        Called when the Start button is pressed.
        '''
        if not self.game_state in ["game over", "continue", "start"]:
            if self.game_state == "running":
                pg.mixer.music.pause()
            elif self.game_state == "pause":
                pg.mixer.music.unpause()
            self.game_state = "pause" if self.game_state == "running" else "running"
        elif self.game_state == "continue":
            self.level.reset()
            pg.mixer.music.play(-1)
            self.game_state = "running"


if __name__ == "__main__":
    clear()
    game = Game()
    game.run()
