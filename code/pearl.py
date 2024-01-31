import pygame
from tiles import StaticTile


class Pearl(StaticTile):
    def __init__(self, size, x, y, direction):
        super().__init__(size, x, y, pygame.image.load('../graphics/enemy/pearl/pearl.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pearl_sprite = pygame.sprite.GroupSingle()
        self.direction = direction
        self.speed = 7
        self.has_hit = False

    def is_pearl_offcamera(self, surface):
        if not self.rect.colliderect(surface.get_rect()):
            self.has_hit = True

    def destroy(self):
        if self.has_hit:
            self.kill()

    def update(self, x_shift, surface=None):
        self.rect.x += x_shift
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        self.is_pearl_offcamera(surface)
        self.destroy()
