import pygame
from tiles import AnimatedTile
from support import import_folder
from pearl import Pearl


class Shell(AnimatedTile):
    def __init__(self, size, x, y, direction):
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

        # if direction == 'left':
        #     self.collision_rect.x -= size
        # else:
        #     self.collision_rect.x += size

    def shoot(self):
        if not self.attack_state:
            print('shot')
            self.time_of_shot = pygame.time.get_ticks()
            # if self.direction == 'left':
            self.frames = self.attack_frames
            self.attack_state = True
            self.pearl = Pearl(self.size, self.rect.centerx, self.rect.y + 10, self.direction)
            # else:
            #     self.frames = import_folder('../graphics/enemy/shell_right/attack')

    def reload_timer(self):
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
        self.rect.x += x_shift
        self.animate()
        self.reload_timer()

