import pygame
from pygame.sprite import Sprite

class Fleet(Sprite):
    """A class to represent a single ship in the enemy fleet."""

    def __init__(self, si_game):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = si_game.screen
        self.settings = si_game.settings

        #Load the image and set its rect attribute
        self.image = pygame.image.load('images/empire.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the top left conner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Stores the horizontal position
        self.x = float(self.rect.x)


    def check_edges(self):
        """Return True if enemy is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Move the fleet to the right"""
        self.x += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.x = self.x