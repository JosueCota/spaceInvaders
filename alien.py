import pygame as pg 
from character import Character
from vector import Vector
from pygame.sprite import Sprite, Group


class Aliens:
    def __init__(self, game):
        self.game = game 
        self.settings = game.settings
        self.screen = game.screen
        self.ship = game.ship
        self.stats = game.stats
        self.aliens = Group()
        self.v = Vector(self.settings.alien_speed_factor, 0)
        self.create_fleet()
        
    def number_aliens_x(self, alien_width): 
        available_space_x = self.settings.screen_width - 1.2 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x
    
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height -
                            (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1.2 * alien_height))
        return number_rows 

    def create_alien(self, alien_number, row_number): 
        alien = Alien(game=self.game)
        alien.x = alien.rect.width + 1.2 * alien.rect.width * alien_number
        alien.y = alien.rect.height + 1.2 * alien.rect.height * row_number
        alien.rect.x, alien.rect.y = alien.x, alien.y
        self.aliens.add(alien)

    def create_fleet(self): 
        alien = Alien(game=self.game)
        number_aliens_x = self.number_aliens_x(alien.rect.width)
        number_rows = self.get_number_rows(self.ship.rect.height, alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def reverse_fleet(self): 
        self.v.x *= -1
        for alien in self.aliens:
            alien.v.x *= -1
            alien.y += self.settings.fleet_drop_speed

    def check_edges(self): 
        for alien in self.aliens:
            if alien.check_edges(): return True
        return False
        
    def check_bottom(self): 
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.screen_height:
                return True 
        return False
        
    def update(self):
        for alien in self.aliens: alien.update()
        if self.check_bottom(): self.game.game_over()
        if self.check_edges(): self.reverse_fleet()
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self.stats.ship_hit()
        self.draw()
            
    def draw(self): 
        for alien in self.aliens:
            alien.draw()


class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen 
        self.settings = game.settings
        self.ship = game.ship
        self.v = Vector(game.settings.alien_speed_factor, 0)
         
        self.image = pg.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self): 
        left, right = self.rect.left, self.rect.right
        return left <= 0 or right >= self.settings.screen_width

    def update(self): 
        self.y += self.v.y
        self.x += self.v.x
        self.rect.x, self.rect.y = self.x, self.y
    
    def draw(self): 
        self.screen.blit(self.image, self.rect) 
