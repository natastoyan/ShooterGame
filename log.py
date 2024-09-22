import pygame as pg
from settings import *



class Log:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font('freesansbold.ttf', 24)
        self.bigger_font = pg.font.Font('freesansbold.ttf', 36)

    def draw(self):
        str = f"Player Angle: {round(self.game.player.angle, 2)} " \
               f"Player moves: {self.game.player.moves}. " \
               f"Player sin {round(self.game.player.sin_a, 2)}. " \
               f"Player cos {round(self.game.player.cos_a, 2)}. " \
               f"Player X {round(self.game.player.x, 2)}. " \
              f"Player Y {round(self.game.player.y, 2)}. " \
              f"Player dX {round(self.game.player.dx, 2)}. " \
              f"Player dY {round(self.game.player.dy, 2)}. "

        text = self.font.render(str, True, 'green', 'blue')
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, 20)
        # self.game.screen.blit(text, textRect)

        health_str = f"Health: {self.game.player.health}"
        health_text = self.bigger_font.render(health_str, True, 'yellow', 'red')
        health_rect = text.get_rect()
        health_rect.top = 30
        health_rect.left = WIDTH - 200

        self.game.screen.blit(health_text, health_rect)