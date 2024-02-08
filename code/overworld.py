"""The overworld.py module manages the game's overworld environment,
    including navigation between levels and player movement on the overworld map.
    The code follows object-oriented principles, with classes (Node, Icon, Overworld)
    encapsulating related behaviours and data.
"""

import pygame
from game_data import levels
from support import import_folder
from decoration import Sky


class Node(pygame.sprite.Sprite):
    """Represents a node on the overworld map, which corresponds to a level in the game.

        Attributes:
            frames: List of images representing the animation frames for the node.
            frame_index: Current index of the animation frame.
            image: Current image representing the node.
            status: Status of the node (available or locked).
            rect: Rectangle representing the position and size of the node.
            detection_zone: Rectangle representing the detection zone for player interaction.
    """
    def __init__(self, pos, status, icon_speed, path):
        """Initializes the node with its position, status, animation speed, and image path.

            Parameters:
                pos: The position of the node sprite.
                status: The status of the node, either 'available' or 'locked'.
                icon_speed: The speed of the associated icon.
                path: The path to the folder containing the node graphics.
        """
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect = self.image.get_rect(center = pos)

        # we need this detection zone, because if the detection zone is too small the icon could miss it due to the speed
        # so we must set the size of the zone relative to the speed, so that it won't jump over it
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

    def animate(self):
        """ Animates the node by cycling through its animation frames."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        """Updates the node's animation and status."""
        if self.status == 'available':
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0, 0))


class Icon(pygame.sprite.Sprite):
    """Represents the player's icon on the overworld map.

        Attributes:
            pos: Position of the icon.
            image: Image representing the icon.
            rect: Rectangle representing the position and size of the icon.
    """
    def __init__(self, pos):
        """ Initializes the icon with its position.

            Parameters:
                pos: The position of the icon sprite.
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """Updates the icon's position."""
        self.rect.center = self.pos


class Overworld:
    """Manages the overworld environment, including node setup, player movement, and level progression.

                Attributes:
                    display_surface: Surface where the overworld map is rendered.
                    max_level: Maximum level accessible in the overworld.
                    current_level: Current level selected by the player.
                    create_level: Callback function to create a level instance.
                    moving: Boolean indicating if the player is currently moving.
                    move_direction: Vector representing the direction of player movement.
                    speed: Speed of player movement.
                    nodes: Group containing all nodes on the overworld map.
                    icon: Group containing the player's icon.
                    sky: Instance of the Sky class representing the sky background.
                    start_time: Time when the level transition started.
                    allow_input: Boolean indicating if player input is allowed.
                    timer_length: Length of the transition timer.
            """

    def __init__(self, start_level, max_level, surface, create_level):
        """Initializes the overworld with starting level, max level, surface, and level creation callback.

            Parameters:
                start_level: The starting level.
                max_level: The maximum level reached.
                surface: The display surface.
                create_level: A function to create a level.
        """

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def setup_nodes(self):
        """Sets up the nodes on the overworld map."""
        self.nodes = pygame.sprite.Group()

        for node_index, node_data in enumerate(levels.values()):
            if node_index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])

            self.nodes.add(node_sprite)

    def setup_icon(self):
        """Sets up the player's icon on the overworld map."""
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        """ Draws paths between unlocked nodes."""
        if self.max_level > 0:
            points = [node['node_pos'] for node_index, node in enumerate(levels.values()) if node_index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def input(self):
        """Handles player input for navigating the overworld"""
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data(1)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data(-1)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, direction):
        """Calculates movement direction vector between nodes.
            Vector calculations are used to determine movement direction and distance,
            ensuring smooth and accurate player movement between nodes.

            Parameters:
                direction: The direction of movement.

            Returns:
                pygame.math.Vector2: The movement data.
        """
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + direction].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        """Updates the position of the player's icon during movement.
            Collision detection is performed using the collidepoint method of the pygame.Rect object
            representing the detection zone. This method checks whether a given point
            (the current position of the player icon) is within the boundaries of the detection zone.
            If the player icon's position collides with the detection zone of the target node, it indicates
            that the player has reached the destination node.
            Upon detecting a collision between the player icon and the detection zone,
            the movement process is halted. The player's current level is updated to the index of the target node,
            indicating a transition to the corresponding level.
        """
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]

            # here we check for collision between the position of the icon and the detection zone
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        """Manages the transition timer for level selection. It is implemented to prevent player input during
            certain periods, adding a delay before the player can move again, for example when the player has died
            but keeps holding one of the arrow keys.
        """
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def run(self):
        """Main loop for running the overworld, handling input, updating positions, and rendering."""
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
