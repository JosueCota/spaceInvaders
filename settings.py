from colors import DARK_GREY, LIGHT_GREY, LIGHT_RED

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = LIGHT_RED

        
        self.laser_width = 3
        self.laser_height = 30
        self.laser_color = 60, 60, 60
        self.lasers_allowed = 3000
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed = 10
        self.alien_speed_factor = 10
        self.laser_speed_factor = 10
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.laser_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points *self.score_scale)
            
