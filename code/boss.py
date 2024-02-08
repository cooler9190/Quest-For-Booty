"""This module defines a class representing the boss enemy in the game."""

import pygame
from tiles import AnimatedTile
from support import import_folder
from math import sin


class Boss(AnimatedTile):
    """Represents the boss enemy in the game.
        Inherits from AnimatedTile class.

        Attributes:
            speed: Speed of the boss.
            health: Health points of the boss.
            invincible: Flag indicating whether the boss is invincible.
            invincibility_duration: Duration of invincibility after being hit.
            hurt_time: Time at which the boss was last hurt.
            alive: Flag indicating whether the boss is alive.
            hit_sound: Sound played when the boss is hit.
    """
    def __init__(self, size, x, y):
        """Initializes a Boss object with a specified size, position, and initial attributes.

            Parameters:
                size: Size of the boss.
                x: X-coordinate of the boss.
                y: Y-coordinate of the boss.
        """
        super().__init__(size, x, y, '../graphics/enemy/boss idle')
        self.rect.y -= 120
        self.speed = 7
        self.idle_frames = import_folder('../graphics/enemy/boss idle')
        self.run_left_frames = import_folder('../graphics/enemy/boss run left')
        self.run_right_frames = import_folder('../graphics/enemy/boss run right')
        self.health = 30
        self.invincible = False
        self.invincibility_duration = 2000
        self.hurt_time = 0
        self.alive = True

        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
        self.hit_sound.set_volume(0.7)

    def move_right(self):
        """Moves the boss to the right and changes the animation frames."""
        self.rect.x += self.speed
        self.frames = self.run_right_frames

    def move_left(self):
        """Moves the boss to the left and changes the animation frames."""
        self.rect.x -= self.speed
        self.frames = self.run_left_frames

    def stop(self):
        """Stops the boss from moving and changes the animation frames to idle."""
        self.frames = self.idle_frames

    def take_damage(self):
        """Inflicts damage on the boss and activates invincibility."""
        if not self.invincible:
            self.hit_sound.play()
            self.health -= 10
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            print("boss health:", self.health)

    def invincibility_timer(self):
        """ Manages the invincibility timer for the boss."""
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        """Calculates a wave value for use in effects.

            Returns:
                Integer representing the alpha value.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def invincibility_blink(self):
        """Implements blinking effect during invincibility."""
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def is_alive(self):
        """Checks if the boss is alive.

            Returns:
                True if the boss is alive, False otherwise.
        """
        if self.health <= 0:
            return False
        else:
            return True

    def is_target_in_height_range(self, y):
        """Checks if a target is within a specified height range.

            Parameters:
                y: Y-coordinate of the target.

            Returns:
                True if the target is within the height range, False otherwise.
        """
        if self.rect.bottom - 192 <= y >= self.rect.top - 64:
            return True
        else:
            return False

    def update(self, x_shift, surface=None):
        """Updates the boss's position and state.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the boss on. Defaults to None.
        """
        self.rect.x += x_shift
        self.animate()
        self.invincibility_blink()
        self.invincibility_timer()
        self.wave_value()
