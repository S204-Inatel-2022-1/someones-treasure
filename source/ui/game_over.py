import pygame as pg


class GameOverScreen:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        font = pg.font.Font("fonts/PixelGameFont.ttf", 64)
        self.text = font.render("GAME OVER", False, "red")
        self.image = pg.image.load("images/game-over/very_sad_rat.png")

    def display(self):
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()
        image_rect = self.image.get_rect(center=(width // 2, height // 2))
        text_rect = self.text.get_rect(center=(width // 2, height * 0.75))
        self.display_surface.blit(self.image, image_rect)
        self.display_surface.blit(self.text, text_rect)
