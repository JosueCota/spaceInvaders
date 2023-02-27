from colors import GREEN, WHITE
import pygame as pg

class Button():
    def __init__(self, game, msg):
        self.screen = game.screen
        self.game = game
        self.screen_rect = self.screen.get_rect()
        self.msg = msg
        self.width, self.height = 200, 50
        self.button_color = GREEN
        self.text_color = WHITE
        self.font = pg.font.SysFont(0, 48)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.game.game_active = False
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def play_game(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.game.play_again()
            return True
       