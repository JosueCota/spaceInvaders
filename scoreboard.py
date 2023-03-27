import pygame as pg 
import pygame.font
import os.path
from ship import Ship
from pygame.sprite import  Group

class Scoreboard:
    def __init__(self, game): 
        self.game = game
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        if not os.path.isfile("./high_score.txt"):
            with open("high_score.txt", "w") as file:
                for i in range(5):
                    file.write("0\n")

        with open("high_score.txt", "r") as file:
            if not file.read(1):
                self.high_score = 0
            else:
                file.seek(0)
                self.high_score = int(file.readline())

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()
        self.prep_high_score()
        self.prep_ship()
    def increment_score(self, n): 
        self.score += n
        self.prep_score()

    def prep_high_score(self):
        self.high_score = round(self.high_score, -1)
        self.high_score_str = "{:,}".format(self.high_score)
        self.high_score_image = self.font.render(self.high_score_str, True, self.text_color,self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_ship(self):
        self.ships = Group()
        for ship in range(self.game.ship.ships_left):
            temp_ship = Ship(self.game)
            temp_ship = Ship.set_ship_lives(temp_ship, ship)
            self.ships.add(temp_ship)

    def reset(self): 
        
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        for ship in self.ships:
            Ship.draw(ship)

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()
        

    def save_highscores(self):
        int_list = []
        with open("high_score.txt", "r") as file: 
            
            lines = [line.rstrip() for line in file]
            int_list = [int(i) for i in lines]
            for n in range(5):
                if int_list[n] <= self.score:
                    int_list.insert(n, self.score)
                    break
                
        with open("high_score.txt", "w") as file:
            for highscores in range(5):
                file.writelines(str(int_list[highscores]) + "\n")
                    
           
