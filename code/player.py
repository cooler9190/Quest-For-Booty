"""The player.py module contains the implementation of the player character in the game,
    including movement, animation, collision handling, and health management.
"""

import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    """Represents the player character in the game.

        Attributes:
            animations: Dictionary containing animation frames for different player states (idle, run, jump, fall).
            frame_index: Index of the current animation frame.
            animation_speed: Speed of animation playback.
            image: Current image representing the player.
            rect: Rectangle representing the position and size of the player.
            dust_run_particles: List of dust particles for running animation.
            dust_frame_index: Index of the current dust particle frame.
            dust_animation_speed: Speed of dust particle animation playback.
            display_surface: Surface where the player is rendered.
            create_jump_particles: Callback function to create jump particles.
            direction: Vector representing the player's movement direction.
            speed: Speed of player movement.
            gravity: Strength of gravity affecting the player.
            jump_speed: Initial speed of the player's jump.
            collision_rect: Rectangle representing the player's collision area.
            status: Current status of the player (idle, run, jump, fall).
            facing_right: Boolean indicating whether the player is facing right.
            on_ground: Boolean indicating whether the player is on the ground.
            on_platform: Reference to the moving platform the player is standing on.
            on_ceiling: Boolean indicating whether the player is touching the ceiling.
            on_left: Boolean indicating whether the player is touching a wall on the left.
            on_right: Boolean indicating whether the player is touching a wall on the right.
            alive: Boolean indicating whether the player is alive.
            change_health: Callback function to change the player's health.
            invincible: Boolean indicating whether the player is invincible.
            invincibility_duration: Duration of invincibility after taking damage.
            hurt_time: Time when the player was last hurt.
            jump_sound: Sound effect for player jumps.
            hit_sound: Sound effect for player taking damage.
"""
    def __init__(self, pos, surface, create_jump_particles, change_health):
        """Initializes the player with starting position, surface, callback functions
            for creating jump particles and changing health.

            Parameters:
                pos: Tuple representing the initial position of the player.
                surface: Pygame surface where the player is rendered.
                create_jump_particles: Callback function to create jump particles.
                change_health: Callback function to change the player's health.
        """
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # in pygame, a vector2 is a list that contains an x and a y value,
        # with which it creates a line and direction to move to2

        # we can add a vector to the position of a rect:
        # rect.center += pygame.math.Vector2(100, 50)
        # the x and y can be accessed separately
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_platform = None
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.alive = True

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
        self.hit_sound.set_volume(0.7)

    def import_character_assets(self):
        """Imports player character animations."""
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        """Imports dust particles for running animation."""
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        """Animates the player based on current status and direction."""
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def run_dust_animation(self):
        """Plays dust particle animation when running."""
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particles = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particles, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particles = pygame.transform.flip(dust_particles, True, False)
                self.display_surface.blit(flipped_dust_particles, pos)

    # To get status of player we can use
    # jump - direction.y < 0
    # fall - direction.y < 0
    # run - direction.y == 0 AND direction.x != 0
    # idle - direction.y == 0 AND direction.x == 0

    def get_status(self):
        """Determines the player's status based on movement and direction."""
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def get_input(self):
        """Handles player input for movement and jumping."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.move_right()
        elif keys[pygame.K_a]:
            self.move_left()
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        """Applies gravity to the player's vertical movement."""
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        """Initiates a jump if the player is on the ground."""
        if self.on_ground:
            self.jump_sound.play()
            self.direction.y = self.jump_speed
            self.create_jump_particles(self.rect.midbottom)

    def move_right(self):
        """Sets the player's movement direction to right."""
        self.direction.x = 1
        self.facing_right = True

    def move_left(self):
        """Sets the player's movement direction to left."""
        self.direction.x = -1
        self.facing_right = False

    def heal(self):
        """Increases the player's health."""
        self.change_health(10)

    def get_damage(self, damage):
        """Deals damage to the player and activates invincibility if not already invincible.

            Parameters:
                damage: Integer representing the amount of damage to apply.
        """
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(damage)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        """Manages the duration of invincibility after taking damage."""
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        """Generates a wave value for creating a flashing effect during invincibility.

            Returns:
                Integer representing the alpha value.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        """Updates the player's state, including animation, input handling, collision, and health management.
            Also checks for the on_platform attribute if it has a value(reference to a specific moving platform)
            the player will move according to the direction and speed of that moving platform.
        """
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()

        if self.on_platform:
            if self.on_platform.move_type == 'horizontal':
                self.collision_rect.x += self.on_platform.speed
            else:
                self.collision_rect.y += self.on_platform.speed

