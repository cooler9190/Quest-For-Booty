"""This module defines a class representing pearls shot by shell enemies."""

import pygame
from tiles import StaticTile


class Pearl(StaticTile):
    """Represents a projectile shot by enemies.
        Inherits from StaticTile class.

        Attributes:
            direction: Direction of the pearl (left or right).
            speed: Speed of the pearl.
            has_hit: Flag indicating whether the pearl has hit a target.
    """
    def __init__(self, size, x, y, direction):
        """Initializes a Pearl object with a specified size, position, and direction.

            Parameters:
                size: Size of the pearl.
                x: X-coordinate of the pearl.
                y: Y-coordinate of the pearl.
                direction: Direction of the pearl (left or right).
        """
        super().__init__(size, x, y, pygame.image.load('../graphics/enemy/pearl/pearl.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pearl_sprite = pygame.sprite.GroupSingle()
        self.direction = direction
        self.speed = 7
        self.has_hit = False

    def is_pearl_offcamera(self, surface):
        """Checks if the pearl has moved off the camera view.

            Parameters:
                surface: Surface representing the game screen.
        """
        if not self.rect.colliderect(surface.get_rect()):
            self.has_hit = True

    def destroy(self):
        """Destroys the pearl if it has hit a target."""
        if self.has_hit:
            self.kill()

    def update(self, x_shift, surface=None):
        """Updates the position of the pearl and checks for collisions.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the pearl on. Defaults to None.
                This parameter is used when updating the pearl.
        """
        self.rect.x += x_shift
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        self.is_pearl_offcamera(surface)
        self.destroy()
