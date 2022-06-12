import pygame as pg


class PauseScreen:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        font = pg.font.Font("fonts/PixelGameFont.ttf", 36)
        self.text = font.render("PAUSED", False, "white")

    def display(self):
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()
        text_rect = self.text.get_rect(center=(width // 2, height // 2))
        self.display_surface.blit(self.text, text_rect)
