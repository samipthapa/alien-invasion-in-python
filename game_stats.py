class GameStats:
    """Track statistics for the game"""

    def __init__(self, si_game):
         self.settings = si_game.settings
         self.reset_stats()
         self.game_active = True


    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit