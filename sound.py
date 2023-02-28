import pygame as pg 
import time


class Sound:
    def __init__(self): 
        # self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        self.background = pg.mixer.Sound('sounds/Tetris.mp3')
        self.death = pg.mixer.Sound('sounds/death.wav')
        self.lasers = pg.mixer.Sound('sounds/laser.wav')
        pg.mixer.Sound.set_volume(self.lasers, 0.1)
        pg.mixer.Sound.set_volume(self.death, 0.3)
        pg.mixer.Sound.play(self.background)
        pg.mixer.Sound.set_volume(self.background, 0.1)
        
                                               
    def play_background(self): 
        pg.mixer.Sound.play(self.background,-1)
        self.music_playing = True
        
    # def play_pickup(self): 
    #     if self.music_playing: self.pickup.play()
        
    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(3.0)       # sleep until game over sound has finished
        
    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def laser_sound(self):
        self.lasers.play()

    def death_sound(self):
        self.death.play()

    def stop_background(self): 
        pg.mixer.Sound.stop(self.background)
        self.music_playing = False 
    
        
    
    
