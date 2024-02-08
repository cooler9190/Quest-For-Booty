"""This module defines a class representing moving platforms used within the game environment.
    Moving platforms can move horizontally or vertically based on their type.
"""

import pygame
from tiles import StaticTile


class MovingPlatform(StaticTile):
    """Represents a moving platform within the game environment.
        Inherits from StaticTile class.

        Attributes:
            Inherits attributes from the StaticTile class.
            speed: Speed of the platform's movement.
            move_type: Type of movement ('horizontal' or 'vertical').
    """
    def __init__(self, size, x, y, path, move_type):
        """Initializes a MovingPlatform object with a given size, position, image path, and movement type.

            Parameters:
                size: Size of the platform (width and height).
                x: X-coordinate of the platform's top-left corner.
                y: Y-coordinate of the platform's top-left corner.
                path: Path to the image representing the platform.
                move_type: Type of movement ('horizontal' or 'vertical').
        """
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
        """Moves the platform horizontally based on its speed."""
        self.rect.x += self.speed

    def move_vertical(self):
        """Moves the platform vertically based on its speed."""
        self.rect.y += self.speed

    def reverse(self):
        """Reverses the direction of the platform's movement."""
        self.speed *= -1

    def update(self, x_shift, surface=None):
        """Updates the position of the platform based on the horizontal shift and moves it according to its type.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the platform.
        """
        self.rect.x += x_shift
        if self.move_type == 'horizontal':
            self.move_horizontal()
        else:
            self.move_vertical()
