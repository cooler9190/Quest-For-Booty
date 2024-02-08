"""This module defines several classes representing different types of tiles
    used within the game environment, such as static tiles, animated tiles, and
    specific objects like crates, rum bottles, etc.
"""
import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    """Base class representing a generic tile in the game.

        Attributes:
            image: Surface representing the tile's image.
            rect: Rectangle representing the position and size of the tile.
"""
    def __init__(self, size, x, y):
        """Initializes a Tile object with a given size and position.

            Parameters:
                size: Size of the tile (width and height).
                x: X-coordinate of the tile's top-left corner.
                y: Y-coordinate of the tile's top-left corner.
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift, surface=None):
        """Updates the position of the tile based on the horizontal shift.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the tile.
        """
        self.rect.x += x_shift


class StaticTile(Tile):
    """Represents a static tile with a fixed image.
        Inherits from Tile class.

        Attributes:
            Inherits attributes from the Tile class.
    """
    def __init__(self, size, x, y, surface):
        """Initializes a StaticTile object with a given size, position, and surface image.

            Parameters:
                size: Size of the tile (width and height).
                x: X-coordinate of the tile's top-left corner.
                y: Y-coordinate of the tile's top-left corner.
                surface: Surface image representing the tile.
        """
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    """Crate class - Represents a crate object within the game environment.
        Inherits from StaticTile class.

        Attributes:
            Inherits attributes from the StaticTile class.
    """
    def __init__(self, size, x, y):
        """Initializes a Crate object with a given size and position.

            Parameters:
                size: Size of the crate (width and height).
                x: X-coordinate of the crate's top-left corner.
                y: Y-coordinate of the crate's top-left corner.
        """
        super().__init__(size, x, y, pygame.image.load('../graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class RumBottle(StaticTile):
    """RumBottle class - Represents a rum bottle object within the game environment.
        Inherits from StaticTile class.

        Attributes:
            Inherits attributes from the StaticTile class.
    """
    def __init__(self, size, x, y):
        """Initializes a RumBottle object with a given size and position.

            Parameters:
                size (int): Size of the rum bottle (width and height).
                x (int): X-coordinate of the rum bottle's top-left corner.
                y (int): Y-coordinate of the rum bottle's top-left corner.
        """
        super().__init__(size, x, y, pygame.image.load('../graphics/terrain/rum_bottle.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Spikes(StaticTile):
    """Spikes class - Represents a spikes obstacle within the game environment.
        Inherits from StaticTile class.

        Attributes:
            Inherits attributes from the StaticTile class.
    """
    def __init__(self, size, x, y):
        """Initializes a Spikes object with a given size and position.

            Parameters:
                size: Size of the spikes (width and height).
                x: X-coordinate of the spikes' top-left corner.
                y: Y-coordinate of the spikes' top-left corner.
        """
        super().__init__(size, x, y, pygame.image.load('../graphics/enemy/spikes/spikes.png').convert_alpha())


class Treasure(StaticTile):
    """Treasure class - Represents a treasure chest object within the game environment.
        Inherits from StaticTile class.

        Attributes:
            Inherits attributes from the StaticTile class.
    """
    def __init__(self, size, x, y):
        """Initializes a Treasure object with a given size and position.

            Parameters:
                size: Size of the treasure chest (width and height).
                x: X-coordinate of the treasure chest's top-left corner.
                y: Y-coordinate of the treasure chest's top-left corner.
        """
        super().__init__(size, x, y, pygame.image.load('../graphics/character/chest.png').convert_alpha())


class AnimatedTile(Tile):
    """AnimatedTile class - Represents an animated tile with multiple frames.
        Inherits from Tile class.

        Attributes:
            frames: List of images representing animation frames.
            frame_index: Current index of the animation frame.
    """
    def __init__(self, size, x, y, path):
        """Initializes an AnimatedTile object with a given size, position, and image path.

            Parameters:
                size: Size of the animated tile (width and height).
                x: X-coordinate of the tile's top-left corner.
                y: Y-coordinate of the tile's top-left corner.
                path: Path to the folder containing animation frames.
        """
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        """Animates the tile by cycling through its frames."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift, surface=None):
        """Updates the position and animation of the tile based on the horizontal shift.

            Parameters:
                x_shift: Horizontal shift amount.
                surface (optional): Surface to render the tile.
        """
        self.animate()
        self.rect.x += x_shift


class Coin(AnimatedTile):
    """Coin class - Represents a coin object within the game environment.
        Inherits from AnimatedTile class.

        Attributes:
            Inherits attributes from the AnimatedTile class.
            value: Value of the coin.
    """
    def __init__(self, size, x, y, path, value):
        """Initializes a Coin object with a given size, position, image path, and value.

            Parameters:
                size: Size of the coin (width and height).
                x: X-coordinate of the coin's top-left corner.
                y: Y-coordinate of the coin's top-left corner.
                path: Path to the folder containing animation frames.
                value: Value of the coin.
        """
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value


class Palm(AnimatedTile):
    """Palm class - Represents a palm tree object within the game environment.
        Inherits from AnimatedTile class.

        Attributes:
            Inherits attributes from the AnimatedTile class.
    """
    def __init__(self, size, x, y, path, offset):
        """Initializes a Palm object with a given size, position, image path, and offset.

            Parameters:
                size: Size of the palm tree (width and height).
                x: X-coordinate of the palm tree's top-left corner.
                y: Y-coordinate of the palm tree's top-left corner.
                path: Path to the folder containing animation frames.
                offset: Vertical offset for positioning the palm tree.
        """
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)
