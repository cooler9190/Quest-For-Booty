"""This module defines classes representing background decorations such as sky, water, and clouds."""

import pygame
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint


class Sky:
    """Represents the sky background decoration.

        Attributes:
            top: Surface representing the top portion of the sky.
            bottom: Surface representing the bottom portion of the sky.
            middle: Surface representing the middle portion of the sky.
            horizon: Y-coordinate of the horizon.
            style: Style of the sky ('level' or 'overworld').
            palms: List of palm tree surfaces and their rectangles.
            clouds: List of cloud surfaces and their rectangles.
    """
    def __init__(self, horizon, style='level'):
        """ Initializes a Sky object with a specified horizon and style.

            Parameters:
                horizon: Y-coordinate of the horizon.
                style (optional): Style of the sky ('level' or 'overworld'). Defaults to 'level'.
        """
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

        self.style = style
        if self.style == 'overworld':
            palm_surfaces = import_folder('../graphics/overworld/palms')
            self.palms = []

            for surface in [choice(palm_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('../graphics/overworld/clouds')
            self.clouds = []

            for surface in [choice(cloud_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * tile_size) - 100)
                #(self.horizon * tile_size) + randint(-100, -50)
                rect = surface.get_rect(midbottom=(x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        """ Draws the sky decorations on the specified surface.

            Parameters:
                surface: Surface to draw the decorations on.
        """
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])

            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])


class Water:
    """Represents the water background decoration.

        Attributes:
            water_sprites: Sprite group containing water tiles.
    """
    def __init__(self, top, level_width):
        """ Initializes a Water object with water tiles.

            Parameters:
                top: Y-coordinate of the top of the water.
                level_width: Width of the level.
        """
        water_start = -screen_width
        water_tile_width = 192
        num_of_tiles = int((level_width + screen_width) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(num_of_tiles):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, '../graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift_x):
        """Draws the water tiles on the specified surface.

            Parameters:
                surface: Surface to draw the water tiles on.
                shift_x: Horizontal shift amount.
        """
        self.water_sprites.draw(surface)
        self.water_sprites.update(shift_x)


class Clouds:
    """Represents the clouds background decoration.

        Attributes:
            cloud_sprites: Sprite group containing cloud tiles.
    """
    def __init__(self, horizon, level_width, cloud_number):
        """Initializes a Clouds object with cloud tiles.

            Parameters:
                horizon: Y-coordinate of the horizon.
                level_width: Width of the level.
                cloud_number: Number of cloud tiles to generate.
        """
        cloud_surf_list = import_folder('../graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift_x):
        """ Draws the cloud tiles on the specified surface.

            Parameters:
                surface: Surface to draw the cloud tiles on.
                shift_x: Horizontal shift amount.
        """
        self.cloud_sprites.draw(surface)
        self.cloud_sprites.update(shift_x)
