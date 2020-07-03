class Settings:
    def __init__(self):
        self.screen_width = 975
        self.screen_height = 650
        self.bg_color = (0, 0, 0)
        self.ship_speed = 2

        #Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 5
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #Fleet settings
        self.enemy_speed = 1.0
        self.fleet_drop_speed = 10
        #1 represents right; -1 represents left
        self.fleet_direction = 1
        