import pygame as pg
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
from start_screen import Start_Game
import sys 

### TODO SHIP LIVES/ HIGHSCORE STORING (NOT RESETTING SCORE PER DEATH) / PLAY BUTTON
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Space Invaders")
        self.game_active = False
        self.highscore_screen = False 
        self.sound = Sound()
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        self.button = Start_Game(self, "PLAY GAME")
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.scoreboard = Scoreboard(game=self) 
        self.aliens = Aliens(game=self)
        
        self.settings.initialize_speed_settings()
        

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        if self.game_active:
            pg.mouse.set_visible(False)
        else:
            pg.mouse.set_visible(True)
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
                elif key == pg.K_m:
                    self.sound.toggle_background()
                elif key == pg.K_q:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()
            elif not self.game_active and not event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if not self.highscore_screen:
                    self.button.hover(mouse_x, mouse_y)
                    self.button.hover_highscore(mouse_x, mouse_y)
                else:
                    self.button.hover_exit_highscore(mouse_x, mouse_y)
                
            elif event.type == pg.MOUSEBUTTONDOWN and not self.game_active:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.game_active = self.button.play_game(mouse_x, mouse_y)
                if not self.highscore_screen: 
                    self.highscore_screen = self.button.scoreboard(mouse_x, mouse_y)
                else:
                    self.highscore_screen = self.button.exit_highscore(mouse_x, mouse_y)
                if self.game_active:
                    self.sound.play_bg()
            if not self.sound.background_channel.get_busy() and self.game_active:
                self.sound.play_bg()
                    

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()
        
    def game_over(self):
        # print('All ships gone: game over!')
        self.sound.background_channel.stop()
        self.sound.gameover()
        self.scoreboard.save_highscores()
        self.scoreboard.score = 0
        self.reset()
        
        self.game_active = False
        print('GAMEOVER...')
        self.button.msg = "PLAY AGAIN?"
        
    def play(self):
        while True:     
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            if self.game_active:    
                self.ship.update()
                self.aliens.update()
                self.barriers.update()
                # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
                self.scoreboard.update()   
            elif not self.highscore_screen:
                self.button.draw_button()
            else:
                self.button.draw_hs_screen()
            pg.display.flip()



def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
