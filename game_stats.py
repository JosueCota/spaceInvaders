import pygame as pg, time

class GameStats():
    def __init__(self, game):
        self.ship_limit = 3
        self.ships_left = 3
        self.game = game
    def reset_stats(self):
        self.ships_left = self.ship_limit

    def ship_hit(self):
        self.ships_left -=1
        
        if self.ships_left == 0:
            self.game.game_over()
        self.game.aliens.aliens.empty()
        self.game.lasers.lasers.empty()
        self.game.aliens.create_fleet()
        self.game.ship.center_ship()

        time.sleep(0.5)

