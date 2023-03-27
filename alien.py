from ast import Or
from email.headerregistry import HeaderRegistry
from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer

class Alien(Sprite): 
    alien_images = [[pg.transform.rotozoom(pg.image.load(f'images/alien1/alien1_{n}.png'), 0, 0.15) for n in range(2)],
                    [pg.transform.rotozoom(pg.image.load(f'images/alien2/alien2_{n}.png'), 0, 0.15) for n in range(2)],
                    [pg.transform.rotozoom(pg.image.load(f'images/alien3/alien3_{n}.png'), 0, 0.15) for n in range(2)]]

    alien_timers = {0 : Timer(image_list=alien_images[0]),
                    1 : Timer(image_list=alien_images[1]),
                    2 : Timer(image_list=alien_images[2])}

    alien_explosion_images = [pg.transform.rotozoom(pg.image.load(f'images/aliens_exp/alienexp_{el}.png'), 0, .15) for el in range(3)]
 

    def __init__(self, game, type, alien_number):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.transform.rotozoom(pg.image.load(f'images/alien1/alien1_0.png'), 0, 0.15)
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.sb = game.scoreboard
        self.dying = self.dead = False
        self.check = 0
        start_index = 0 if alien_number % 2 == 0 else 1
        self.timer_normal = Alien.alien_timers[type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, delay=300, is_loop=False)
        self.timer = self.timer_normal     

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    
    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            if self.type == 0:
                self.sb.increment_score(30)
            elif self.type == 1:
                self.sb.increment_score(20)
            elif self.type == 2:
                self.sb.increment_score(10)
            self.game.scoreboard.check_high_score()

    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.rect.centerx, self.rect.centery
        self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=0, alien_number=0)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.ufo_hit = False
        self.ship_lasers = game.ship_lasers.lasers    # a laser Group
        self.aliens_lasers = game.alien_lasers

        self.ufo = Group()
        self.ufo_spawn = randint(500,6000)

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows        

    def reset(self):
        # pass
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
        self.reset_ufo()
    
    def reset_ufo(self):
        self.game.sound.ufo_sound(False)
        self.ufo.empty()
        self.ufo_spawn = randint(500,6000)
        self.ufo_hit = False

    def create_alien(self, alien_number, row_number):
        type = row_number // 2
        alien = Alien(game=self.game, type=type, alien_number=alien_number)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number 
        alien.rect.centery +=100
        self.aliens.add(alien)     

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                   self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return
    
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

        if self.ufo_hit:
            self.reset_ufo()

    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()
                self.game.sound.death_sound()

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        collisions = pg.sprite.groupcollide(self.ufo, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()
                self.ufo_hit = True
                self.game.sound.ufo_sound(False)
            self.game.sound.death_sound()

        # aliens_lasers collide with barrier?
        # ship_lasers collide with barrier?
        collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers, True, True)
        if collisions:
            for laser in collisions:
                laser.kill()

    def ufo_move(self):
        if not self.ufo_hit:
            for ufo in self.ufo:
                ufo.rect.x +=1

    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.ufo_move()
        self.ufo_spawn -= 1
        if self.ufo_spawn == 0:
            self.ufo.add(UFO(game=self.game))
            self.game.sound.ufo_sound(True)
        self.ufo.update()

        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update()      
                
        self.aliens_lasers.update()

    def draw(self): 
        for alien in self.aliens.sprites():
            alien.draw() 


class UFO(Sprite):
    ufo_images = [pg.transform.rotozoom(pg.image.load(f'images/ufo/ufo_{n}.png'), 0, .15) for n in range(2)]
   
    ufo_explosion_images = [pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_{n}.png'), 0, .15) for n in range(6)]
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.ship_lasers = game.ship_lasers.lasers

        self.image = pg.transform.rotozoom(pg.image.load(f'images/ufo/ufo_0.png'), 0, .15)
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = (0, 40)  
        self.x = float(self.rect.x)

        self.timer_normal = Timer(image_list=UFO.ufo_images)
        self.timer_explosion = Timer(image_list=UFO.ufo_explosion_images, delay=200, is_loop=False)  
        self.timer = self.timer_normal    
        self.dying = self.dead = False
    def rand_display(self, n):
        ufo_exp = {0 : pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_0.png'), 0, .15),
               1 : pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_1.png'), 0, .15),
               2 : pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_2.png'), 0, .15),
               3: pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_3.png'), 0, .15),
               4 : pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_4.png'), 0, .15)}
        ufo_pts = {0: 200, 1:100, 2:300, 3:150, 4:50 }
        self.game.scoreboard.increment_score(ufo_pts[n])
        self.ufo_rand = [ufo_exp[n], ufo_exp[n], pg.transform.rotozoom(pg.image.load(f'images/ufo_exp/ufo_exp_5.png'), 0, .15)]

    def hit(self):
        if not self.dying:
            self.rand_display(randint(0,4))
            self.dying = True 
            self.timer_explosion = Timer(image_list=self.ufo_rand, delay=200, is_loop=False)
            self.timer = self.timer_explosion
            if self.timer == self.timer_explosion and self.timer.is_expired():
                self.game.sound.ufo_sound(check=False)
                self.kill()
                self.game.sound.death_sound()
                

    def check_edge(self):
        screen_rect = self.game.screen.get_rect()
        if self.rect.right >= screen_rect.right+50:
            self.game.sound.ufo_sound(check=False)
            self.kill()
            
    
    def update(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.rect.centerx, self.rect.centery+100
        self.screen.blit(image, rect)
        self.check_edge()
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.remove()
        self.posn += (0,1)
        self.draw()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        rect.top -= 50                                      
        self.screen.blit(image, rect)
