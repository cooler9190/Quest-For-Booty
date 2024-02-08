"""The UI class in ui.py  handles the graphical user interface elements of the game,
    including health display and coin count. It provides essential functionality for displaying health and coin
    information to the player during gameplay.
"""
import pygame


class UI:
    """Manages the user interface elements such as health bar and coin display.

        Attributes:
            display_surface: Surface where UI elements are rendered.
            health_bar: Image representing the health bar.
            health_bar_topleft: Top-left position of the health bar.
            bar_max_width: Maximum width of the health bar.
            bar_height: Height of the health bar.
            coin_img: Image representing the coin icon.
            coin_rect: Rectangle representing the position of the coin icon.
            font: Font for rendering text.
    """
    def __init__(self, surface):
        """Initializes UI attributes and loads necessary images and fonts.

            Parameters:
                surface (pygame.Surface): Surface where UI elements are rendered.
        """
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        # where the healthbar starts
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin_img = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin_img.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF', 30)

    def show_health(self, current_health, full_health):
        """Renders the health bar on the display surface.
            It first draws the health bar image at a specified position on the display surface.
            Then, it calculates the current health ratio and adjusts the width of the health bar
            accordingly using a rectangle.
            Finally, it fills the health bar rectangle with a red colour representing the current health level.

            Parameters:
                current_health: Current health value.
                full_health: Maximum health value.
        """
        self.display_surface.blit(self.health_bar, (20, 10))
        # health percentage
        current_health_ratio = current_health / full_health
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        """Renders the coin icon and amount on the display surface.
            The show_coins method displays the coin icon and the current coin count on the screen.
            It blits the coin icon onto the display surface at a predefined position.
            Then, it renders the coin count text using the initialized font and displays it next to the coin icon.

            Parameters:
                amount: Number of coins to display.
        """
        self.display_surface.blit(self.coin_img, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, 'black')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
