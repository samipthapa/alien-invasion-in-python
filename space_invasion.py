import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from fleet import Fleet

class SpaceInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Space Invasion")

        #Creates an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.fleet = pygame.sprite.Group()
        self._create_fleet()


    def start_game(self):
        """Executes the main loop of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()    
                self._update_fleet()
            self._update_screen()
            
            
    def _update_bullets(self):
        """Updates position of bullets and deletes old bullets"""
        self.bullets.update()

        #Get rid of the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_enemy_collision()


    def _check_bullet_enemy_collision(self):
        """Respond to bullet-enemy collision"""
        #The two True delete the bullet and the enemy respectively 
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.fleet, True, True)

        if not self.fleet:
            #Destroy existing bullets and creates new fleet
            self.bullets.empty()
            self._create_fleet()
        

    def _update_fleet(self):
        """Updates the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.fleet.update()
        if pygame.sprite.spritecollideany(self.ship, self.fleet):
            self._ship_hit()

        #Look for fleet hitting the bottom of the screen
        self._check_fleet_bottom()
    

    def _ship_hit(self):
        """Respond to the ship being hit by enemy"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #Look for enemy-ship collison

            #Get rid of any remaining fleet and bullets
            self.fleet.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False


    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                    

    def _check_keydown_events(self, event):
        """Responds to keypress"""
        if event.key  == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    

    def _check_keyup_events(self, event):
        """Responds to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _fire_bullet(self):
        """Creates an instance of Bullet and adds it to the bullets group"""
        if len(self.bullets)  < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.fleet.draw(self.screen)
        #Makes the most recently drawn screen visible
        pygame.display.flip()

    
    def _create_fleet(self):
        """Creates the fleet of enemies."""
        #Creates an enemy and find the number of enemies in a row
        #Spacing between each ship is equal to one ship width
        enemy = Fleet(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width - (2 * enemy_width)
        number_enemies_x = available_space_x //  (2 * enemy_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * enemy_height) - ship_height
        number_rows = available_space_y // (2 * enemy_height)

        #Creates the full fleet
        for row_number in range(number_rows):
            for enemy_number in range(number_enemies_x):
                self._create_enemy(enemy_number, row_number)            

    
    def _create_enemy(self, enemy_number, row_number):
        """Creates an enemy and place it in a row"""
        enemy = Fleet(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = 0.5 * enemy.rect.height + 2 * enemy.rect.height *  row_number
        self.fleet.add(enemy)


    def _check_fleet_edges(self):
        """Responds appropriately if any ships have reached an edge"""
        for enemy in self.fleet.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break   

    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for enemy in self.fleet.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_fleet_bottom(self):
        """Check if the fleet has reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for enemy in self.fleet.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break


if __name__ == '__main__':
    si = SpaceInvasion()
    si.start_game() 