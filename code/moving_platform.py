import pygame
from tiles import StaticTile


class MovingPlatform(StaticTile):
    def __init__(self, size, x, y, path, move_type):
        super().__init__(size, x, y, pygame.image.load(path).convert_alpha())
        if path == '../graphics/terrain/moving_platforms/horizontal_platform.png':
            offset_x = x + 2 * size
            self.rect = self.image.get_rect(topleft=(offset_x, y))
        elif path == '../graphics/terrain/moving_platforms/vertical_platform.png':
            offset_y = y - 2 * size
            self.rect = self.image.get_rect(topleft=(x, offset_y))
        self.speed = 2
        self.move_type = move_type

    def move_horizontal(self):
        self.rect.x += self.speed

    def move_vertical(self):
        self.rect.y += self.speed

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift, surface=None):
        self.rect.x += x_shift
        if self.move_type == 'horizontal':
            self.move_horizontal()
        else:
            self.move_vertical()
