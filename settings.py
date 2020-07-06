class Settings:
    def __init__(self):
        """Initialize the game's static settings"""
        self.screen_width = 975
        self.screen_height = 650
        self.bg_color = (0, 0, 0)
        
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 5
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #Fleet settings
        self.fleet_drop_speed = 15
        
        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quickly the enemy point values increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.enemy_speed = 1.0

        #1 represents right; -1 represents left
        self.fleet_direction = 1

        #Scoring
        self.enemy_points = 10


    def increase_speed(self):
        """Increase speed settings and point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)