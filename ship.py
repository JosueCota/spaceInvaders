import pygame as pg
from pygame.sprite import Sprite, Group
from character import Character
from vector import Vector


class Ship(Character):
    def __init__(self, game):
        super().__init__(game=game, rect=None, v=Vector())
        self.screen = game.screen
        self.settings = game.settings
        
        self.lasers = None
        self.firing = False
        
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
    def set_lasers(self, lasers): self.lasers = lasers 
    
    def fire(self): 
        if len(self.lasers.lasers) < self.settings.lasers_allowed:
            self.lasers.add() 

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom   
        
    def open_fire(self): self.firing = True
    
    def cease_fire(self): self.firing = False
    
    def update(self): 
        super().update()
        if self.firing: 
            self.fire()
            self.game.sound.laser_sound()

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Ship_sb(Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.screen = game.screen 
        self.settings = game.settings
        
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def set_ships(self, ship_num):
        self.rect.x = 10 + ship_num * self.rect.width
        return(self)
        
        

