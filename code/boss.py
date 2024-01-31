import pygame
from tiles import AnimatedTile
from support import import_folder
from math import sin


class Boss(AnimatedTile):
    def __init__(self, size, x, y):
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
        self.rect.x += self.speed
        self.frames = self.run_right_frames

    def move_left(self):
        self.rect.x -= self.speed
        self.frames = self.run_left_frames

    def stop(self):
        self.frames = self.idle_frames

    def take_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.health -= 10
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            print("boss health:", self.health)

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def invincibility_blink(self):
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def is_alive(self):
        if self.health <= 0:
            return False
        else:
            return True

    def is_target_in_height_range(self, y):
        if self.rect.bottom - 192 <= y >= self.rect.top - 64:
            return True
        else:
            return False

    def update(self, x_shift, surface=None):
        self.rect.x += x_shift
        self.animate()
        self.invincibility_blink()
        self.invincibility_timer()
        self.wave_value()
