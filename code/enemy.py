"""This module defines a class representing enemy walkers that can move and interact with the player."""

import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    """Represents an enemy entity in the game.
        Inherits from AnimatedTile class.

        Attributes:
            speed (int): Speed of the enemy entity.
    """
    def __init__(self, size, x, y):
        """Initializes an Enemy object with a specified size and position.

            Parameters:
                size: Size of the enemy entity.
                x: X-coordinate of the enemy entity.
                y: Y-coordinate of the enemy entity.
        """
        super().__init__(size, x, y, '../graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)

    def move(self):
        """Moves the enemy entity horizontally according to its speed."""
        self.rect.x += self.speed

    def reverse_image(self):
        """Reverses the image of the enemy entity if it is moving in the opposite direction."""
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Reverses the direction of movement of the enemy entity."""
        self.speed *= -1

    def update(self, x_shift, surface=None):
        """Updates the position and animation of the enemy entity.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the enemy entity on. Defaults to None.
        """
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()


