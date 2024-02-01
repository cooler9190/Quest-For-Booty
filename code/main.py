import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI


class Game:
    def __init__(self):
        # game attributes
        self.max_level = 4
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
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
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
        self.coin_amount += amount

    def change_health(self, amount):
        if self.current_health != self.max_health or amount < 0:
            self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coin_amount = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
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
