"""This module defines a class representing various particle effects used in the game."""

import pygame
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    """Represents a particle effect with animation and movement.

        Attributes:
            frame_index: Index of the current frame in the animation.
            animation_speed: Speed of animation playback.
            frames: List of frames for the particle effect animation.
            image: Current frame image of the particle effect.
            rect: Rectangle representing the position and size of the particle effect.
    """
    def __init__(self, pos, type):
        """Initializes a ParticleEffect object with a specified position and type.

            Parameters:
                pos: Position of the particle effect.
                type: Type of the particle effect ('jump', 'land', 'explosion').
        """
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5

        if type == 'jump':
            self.frames = import_folder('../graphics/character/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder('../graphics/character/dust_particles/land')
        if type == 'explosion':
            self.frames = import_folder('../graphics/enemy/explosion')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """Advances the animation frame and updates the particle effect image."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        """ Updates the particle effect's position and animation.

            Parameters:
                x_shift: Horizontal shift amount.
        """
        self.animate()
        self.rect.x += x_shift
