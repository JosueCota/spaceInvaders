import pygame as pg

class Start_Game():
    def __init__(self, game, msg):
        self.screen = game.screen
        self.game = game
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()
        
        self.title1pos = (self.settings.screen_width/2, (self.settings.screen_height/3)-(self.settings.screen_height/5))
        self.title2pos = (self.settings.screen_width/2, (self.settings.screen_height/3)-(self.settings.screen_height/11))
        self.hs_pos = (self.settings.screen_width/2, self.settings.screen_height-100)
        self.msg = msg
        self.width, self.height = 200, 50

        self.bg_color = game.settings.bg_color   #Black
        self.text_color = (255, 255, 255)   #White

        self.font = pg.font.SysFont(0, 50)
        self.score_font = pg.font.SysFont(0,40)
        self.highscore_font = pg.font.SysFont(0, 75)
        self.hs_screen_font = (128,0,0)
        
        self.rect_title = pg.Rect(0,0, 200, 50)
        self.rect_title2 = pg.Rect(0,0,200, 50)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.settings.screen_width/2, self.settings.screen_height-200)
        self.rect_hs = pg.Rect(0,0,200,50)
    
        self.highscore_button()
        self.prep_msg()
        self.prep_title()
        self.alien_scores()
        self.alien_images()

    def prep_title(self):
        self.title_font = pg.font.SysFont(0, 200)
        self.space_text = self.title_font.render('SPACE', True, self.text_color, self.bg_color)
        self.space_text_rect = self.space_text.get_rect()
        self.space_text_rect.center = self.title1pos

        self.title_font2 = pg.font.SysFont(0, 100)
        self.space_text2 = self.title_font2.render('INVADERS', True, (0,255,0), self.bg_color)
        self.space_text2_rect = self.space_text2.get_rect()
        self.space_text2_rect.center = self.title2pos 

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
 
    def highscore_button(self):
        self.hs_font = pg.font.SysFont(0, 50)
        self.hs_image = self.hs_font.render("HIGH SCORES", True, self.text_color, self.bg_color)
        self.hs_image_rect = self.hs_image.get_rect()
        self.hs_image_rect.center = self.hs_pos
    
    def highscore_screen_button(self):
        self.hscreen_font = pg.font.SysFont(0, 80)
        
        self.hscreen_image = self.hscreen_font.render("HIGH SCORES", True, self.hs_screen_font, self.bg_color)
        self.hscreen_image_rect = self.hscreen_image.get_rect()
        self.hscreen_image_rect.center = (600, 100)

    def alien_images(self):
        self.alien1img = pg.transform.rotozoom(pg.image.load(f'images/alien1/alien1_0.png'), 0, 0.12)
        self.alien2img = pg.transform.rotozoom(pg.image.load(f'images/alien2/alien2_0.png'), 0, 0.12)
        self.alien3img = pg.transform.rotozoom(pg.image.load(f'images/alien3/alien3_0.png'), 0, 0.12)
        self.alien4img = pg.transform.rotozoom(pg.image.load(f'images/ufo/ufo_0.png'), 0, 0.12)
        self.x, self.y = 505, 250

    def alien_scores(self):
        self.alien1_score = self.score_font.render("= 30 PTS", True, self.text_color, self.bg_color)
        self.alien1_score_rect= self.alien1_score.get_rect()
        self.alien1_score_rect.center = (630,275)

        self.alien2_score = self.score_font.render("= 20 PTS", True, self.text_color, self.bg_color)
        self.alien2_score_rect= self.alien2_score.get_rect()
        self.alien2_score_rect.center = (630,350)

        self.alien3_score = self.score_font.render("= 10 PTS", True, self.text_color, self.bg_color)
        self.alien3_score_rect= self.alien3_score.get_rect()
        self.alien3_score_rect.center = (630,425)

        self.alien4_score = self.score_font.render("= ???", True, self.text_color, self.bg_color)
        self.alien4_score_rect= self.alien4_score.get_rect()
        self.alien4_score_rect.center = (610,500)

    def highscore_display(self):
        with open("high_score.txt", "r") as file:
            highscore_list = [line.rstrip() for line in file]
                
        self.highscore1 = self.highscore_font.render(highscore_list[0], True, self.text_color, self.bg_color) 
        self.highscore2 = self.highscore_font.render(highscore_list[1], True, self.text_color, self.bg_color) 
        self.highscore3 = self.highscore_font.render(highscore_list[2], True, self.text_color, self.bg_color) 
        self.highscore4 = self.highscore_font.render(highscore_list[3], True, self.text_color, self.bg_color) 
        self.highscore5 = self.highscore_font.render(highscore_list[4], True, self.text_color, self.bg_color) 
                
    
    def draw_button(self):
        if not self.game.highscore_screen:
            self.screen.fill(self.bg_color, self.rect)
            self.screen.blit(self.msg_image, self.msg_image_rect)

            self.screen.blit(self.space_text, self.space_text_rect)
            self.screen.blit(self.space_text2, self.space_text2_rect)
            self.screen.blit(self.hs_image, self.hs_image_rect)

            self.screen.blit(self.alien1_score, self.alien1_score_rect)
            self.screen.blit(self.alien2_score, self.alien2_score_rect)
            self.screen.blit(self.alien3_score, self.alien3_score_rect)
            self.screen.blit(self.alien4_score, self.alien4_score_rect)

            self.screen.blit(self.alien1img, (self.x,self.y))
            self.screen.blit(self.alien2img, (self.x+8,self.y+75))
            self.screen.blit(self.alien3img, (self.x+8,self.y+150))
            self.screen.blit(self.alien4img, (self.x,self.y+235))
        else:
            self.screen.blit(self.hscreen_image, self.hscreen_image_rect)

            self.screen.blit(self.highscore1, (525, 200))
            self.screen.blit(self.highscore2, (525, 275))
            self.screen.blit(self.highscore3, (525, 350))
            self.screen.blit(self.highscore4, (525, 425))
            self.screen.blit(self.highscore5, (525, 500))
    
    def draw_hs_screen(self):
        self.highscore_display()
        self.highscore_screen_button()
        self.draw_button()
        
    def exit_highscore(self,x, y):
        if self.hscreen_image_rect.collidepoint(x,y):
            return False
        else:
            return True

    def hover_exit_highscore(self ,x, y):
        if self.hscreen_image_rect.collidepoint(x, y):
            self.hs_screen_font = (128,0,0)
            self.highscore_screen_button()
        else:
            self.hs_screen_font = (255,255,255)
            self.highscore_screen_button()

    def hover_highscore(self,x ,y):
        if self.hs_image_rect.collidepoint(x, y):
            self.text_color = (0,255,0)
            self.highscore_button()
        else:
            self.text_color = (255, 255, 255)
            self.highscore_button()

    def hover(self, x, y):
        if self.msg_image_rect.collidepoint(x, y):
            self.text_color = (255,255,255)
            self.prep_msg()
        else:
            self.text_color = (0, 255, 0)
            self.prep_msg()
    
    def scoreboard(self,x ,y):
        if self.hs_image_rect.collidepoint(x, y):
            return True

    def play_game(self, mouse_x, mouse_y):
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else: 
            return False