from colors import DARK_GREY, LIGHT_GREY, LIGHT_RED

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = LIGHT_RED

        self.ship_speed = 10

        self.alien_speed_factor = 10
        self.fleet_drop_speed = 10

        self.laser_speed_factor = 6
        self.laser_width = 3
        self.laser_height = 30
        self.laser_color = 60, 60, 60
        self.lasers_allowed = 3000
        
