import pygame.font
import os.path
from pygame.sprite import Group

class Scoreboard():
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        if not os.path.isfile("./high_score.txt"):
            with open("high_score.txt", "w") as file:
                print("Created File")

        with open("high_score.txt", "r") as file:
            if not file.read(1):
                self.high_score = 0
            else:
                file.seek(0)
                self.high_score = int(file.read())

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_high_score(self):
        self.high_score = round(self.high_score, -1)
        self.high_score_str = "{:,}".format(self.high_score)
        self.high_score_image = self.font.render(self.high_score_str, True, self.text_color,self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """Turn the score into a rendered image."""
        self.rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(self.rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

         # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.settings.bg_color)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def check_high_score(self):
        if self.stats.score > self.high_score:
            self.high_score = self.stats.score
            
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))
            self.prep_high_score()
