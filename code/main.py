"""The main.py module serves as the entry point for the game execution.
    It initializes the game environment, handles user input, and manages the game loop.
    The code is structured in an object-oriented manner, with a clear separation of concerns.
    Each class (Game, Overworld, Level, UI) handles specific aspects of the game, making the code modular
    and easier to maintain and add new features.
"""

import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI


class Game:
    """Manages the overall game state, including level progression, player status, and user interface.

        Attributes:
            max_level: Maximum level reached in the game.
            max_health: Maximum health points of the player.
            current_health: Current health points of the player.
            coin_amount: Total number of coins collected by the player.
            level_bg_music: Background music for levels.
            overworld_bg_music: Background music for the overworld.
            overworld: Instance of the Overworld class representing the game's overworld environment.
            status: Current status of the game (overworld or level).
            ui: User interface instance for displaying health and coins.
    """
    def __init__(self):
        """ Initializes game attributes and creates necessary instances."""
        # game attributes
        self.max_level = 5
        self.max_health = 100
        self.current_health = 100
        self.coin_amount = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.level_bg_music.set_volume(0.5)
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.5)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

        # ui
        self.ui = UI(screen)

    def create_level(self, current_level):
        """Creates a new level instance."""
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        """ Creates a new overworld instance."""
        if new_max_level == 6:
            pygame.quit()
            sys.exit()
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops=-1)

    def change_coins(self, amount):
        """Updates the coin count by the specified amount."""
        self.coin_amount += amount

    def change_health(self, amount):
        """Updates the player's health by the specified amount."""
        if self.current_health != self.max_health or amount < 0:
            self.current_health += amount

    def check_game_over(self):
        """Checks if the game is over (player health reaches zero) and restarts the game from first level."""
        if self.current_health <= 0:
            self.current_health = 100
            self.coin_amount = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        """Main game loop that handles game state updates and rendering."""
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coin_amount)
            self.check_game_over()


# Pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()

    pygame.display.update()
    clock.tick(60)
