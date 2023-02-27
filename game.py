import pygame as pg, sys, time
from vector import Vector
from sound import Sound
from settings import Settings 
from ship import Ship
from laser import Lasers
from alien import Aliens
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class Game:
    def __init__(self): 
        pg.init()
        self.settings = Settings()
        
        self.window_height, self.window_width = self.settings.screen_height, self.settings.screen_width
        self.screen = pg.display.set_mode((self.window_width, self.window_height), 0, 32)
        pg.display.set_caption('Alien Invasion')
        self.game_active = False
        self.finished = False

        self.button = Button(game=self, msg="Play")
        self.stats = GameStats(game=self)
        self.sound = Sound()
        self.sound.play_background()
        self.button.prep_msg()
        self.scoreboard = Scoreboard(game=self)

        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_lasers(lasers=self.lasers)   

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
                elif key == pg.K_q:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.game_active = self.button.play_game(mouse_x, mouse_y)
                if self.game_active:
                    pg.mouse.set_visible(False)
                else:
                    pg.mouse.set_visible(True)          

 
    def game_over(self):
        self.finished = True
        self.sound.play_gameover()
        self.sound.stop_background()
        pg.quit()
        sys.exit()

    def play_again(self): 
        self.stats.reset_stats()
        self.settings.init_dynamic_settings()
        self.aliens.aliens.empty()
        self.lasers.lasers.empty()

        self.aliens.create_fleet()
        self.ship.center_ship()
        
    def play(self):
        while not self.finished:
            
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            if not self.game_active:
                self.button.draw_button()
            if self.game_active:
                self.scoreboard.show_score()
                self.ship.update()
                self.lasers.update()
                self.lasers.update_bullets()
                self.aliens.update()
            pg.display.update()
            
            time.sleep(0.02)


def main():
    g = Game()
    g.play()
    
    
if __name__ == '__main__':
    main()

 