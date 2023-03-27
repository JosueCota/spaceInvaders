import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self):
        pg.mixer.init(frequency=188200)
        self.music_playing = False

        self.bg_music = pg.mixer.Sound('sounds/Tetris.mp3')
        lasers = pg.mixer.Sound('sounds/laser.wav')
        self.death = pg.mixer.Sound('sounds/death.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
        alien_laser = pg.mixer.Sound('sounds/beam.mp3')
        self.ufo = pg.mixer.Sound('sounds/ufo.mp3')
        self.bg_music_fast = pg.mixer.Sound('sounds/Tetris2.mp3')
        self.bg_music_faster = pg.mixer.Sound('sounds/Tetris3.mp3')

        self.background_channel = pg.mixer.Channel(0)
        pg.mixer.Sound.set_volume(self.death, 0.15)
        pg.mixer.Sound.set_volume(self.bg_music, 0.1)
        pg.mixer.Sound.set_volume(self.bg_music_fast, 0.1)
        pg.mixer.Sound.set_volume(self.bg_music_faster, 0.1)
        pg.mixer.Sound.set_volume(lasers, 0.05)
        pg.mixer.Sound.set_volume(alien_laser, 0.5)
        pg.mixer.Sound.set_volume(self.ufo, .1)
        
        self.sounds = {'alien_laser' : alien_laser, 
                       'lasers': lasers, 'death': self.death,
                       'gameover': gameover_sound}

    def play_bg(self):
        self.background_channel.play(self.bg_music)
        self.music_playing = True

        self.background_channel.queue(self.bg_music_fast)
        self.background_channel.queue(self.bg_music_faster)


    def stop_background(self):
        pg.mixer.Sound.stop(self.bg_music)
        self.music_playing = False 

    def death_sound(self):
        pg.mixer.Sound.play(self.sounds['death'])

    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_bg()

    def ufo_sound(self, check):
        if check:
            pg.mixer.Sound.play(self.ufo,1)
        else:
            pg.mixer.Sound.stop(self.ufo)

    def shoot_laser(self, type): 
        pg.mixer.Sound.play(self.sounds['alien_laser' if type == LaserType.ALIEN else 'lasers'])

    def gameover(self): 
        self.stop_background() 
        pg.mixer.Sound.play(self.sounds['gameover'])
        time.sleep(1.4)
