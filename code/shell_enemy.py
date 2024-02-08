"""This module defines a class representing shell enemies that can shoot projectiles(pearls)."""

import pygame
from tiles import AnimatedTile
from support import import_folder
from pearl import Pearl


class Shell(AnimatedTile):
    """Represents a shell enemy in the game.
        Inherits from AnimatedTile class.

        Attributes:
            direction: Direction of the shell enemy (left or right).
            size: Size of the shell enemy.
            pearl: Projectile fired by the shell enemy.
            reload_time: Time interval for reloading after shooting.
            time_of_shot: Time when the shell enemy last shot a projectile.
            attack_state: Flag indicating whether the shell enemy is in attack state.
            idle_frames: List of idle animation frames for the shell enemy.
            attack_frames: List of attack animation frames for the shell enemy.
    """
    def __init__(self, size, x, y, direction):
        """Initializes a Shell object with a specified size, position, and direction.

            Parameters:
                size: Size of the shell enemy.
                x: X-coordinate of the shell enemy.
                y: Y-coordinate of the shell enemy.
                direction: Direction of the shell enemy (left or right).
        """
        super().__init__(size, x, y, '../graphics/enemy/shell_' + direction + '/idle')

        self.direction = direction
        self.size = size
        self.pearl = None
        self.rect.y += size - self.image.get_size()[1]
        #self.collision_rect = self.rect.copy()
        self.reload_time = 1500
        self.time_of_shot = 0
        self.attack_state = False
        self.idle_frames = import_folder('../graphics/enemy/shell_' + self.direction + '/idle')
        self.attack_frames = import_folder('../graphics/enemy/shell_' + self.direction + '/attack')

    def shoot(self):
        """Initiates a shooting action by the shell enemy if not in attack state."""
        if not self.attack_state:
            print('shot')
            self.time_of_shot = pygame.time.get_ticks()
            # if self.direction == 'left':
            self.frames = self.attack_frames
            self.attack_state = True
            self.pearl = Pearl(self.size, self.rect.centerx, self.rect.y + 10, self.direction)

    def reload_timer(self):
        """Manages the reloading timer for the shell enemy."""
        if self.attack_state:
            # if self.direction == 'left':
            # else:
            #     self.frames = import_folder('../graphics/enemy/shell_right/idle')
            current_time = pygame.time.get_ticks()
            print('tick')
            if current_time - self.time_of_shot >= self.reload_time:
                self.attack_state = False
                self.frames = self.idle_frames

    def update(self, x_shift, surface=None):
        """Updates the position and animation of the shell enemy.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the shell enemy on. Defaults to None.
        """
        self.rect.x += x_shift
        self.animate()
        self.reload_timer()

