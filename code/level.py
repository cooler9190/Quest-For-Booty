import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from moving_platform import MovingPlatform
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # general setup
        self.display_surface = surface
        self.world_shift_x = 0
        self.world_shift_y = 0

        # audio
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.5)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.7)

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # ui
        self.change_coins = change_coins

        # dust particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # moving platforms
        moving_platform_layout = import_csv_layout(level_data['moving platform'])
        self.moving_platform_sprites = self.create_tile_group(moving_platform_layout, 'moving platform')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coins_layout, 'coins')

        # foreground palms setup
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # background palms setup
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # enemy setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # enemy constraint setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # decoration
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    elif type == 'moving platform':
                        sprite = MovingPlatform(tile_size, x, y, 'horizontal')

                    elif type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    elif type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    elif type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/gold', 5)
                        else:
                            sprite = Coin(tile_size, x, y, '../graphics/coins/silver', 1)

                    elif type == 'fg_palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_small', 38)
                        else:
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_large', 64)

                    elif type == 'bg_palms':
                        sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_bg', 64)

                    elif type == "enemies":
                        sprite = Enemy(tile_size, x, y,)

                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                elif val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def platform_collision_reverse(self):
        # earthquake effect
        # pygame.sprite.spritecollide(platform, self.moving_platform_sprites, False)
        for platform in self.moving_platform_sprites:
            if pygame.sprite.spritecollide(platform, self.constraint_sprites, False):
                platform.reverse()

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # In order to fix the problem with where the collision happened
    # we must separate the vertical and horizontal movements and collisions
    # 1. apply vertical movement
    # 2. check vertical collisions
    # 3. apply horizontal movement
    # 4. check horizontal collisions

    # We will move the player and check for collisions here in the level class
    # because we need access to the tiles
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.moving_platform_sprites.sprites()

        for sprite in collidable_sprites:
            # We use colliderect instead of sprite collision because we want to have access to each of the tile's rect
            # and with spritecollide would be a bit more difficult
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    # if direction is left we move the player exactly on the right of the collided object
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                elif player.direction.x > 0:
                    # if direction is right we move the player exactly on the left of the collided object
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.moving_platform_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    # Once we hit a tile we reset the gravity to 0, so that it doesn't build up and destroy the player
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    # When we jump and hit a tile, we must reset the negative y, so that it doesn't increase
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3 and direction_x < 0:
            self.world_shift_x = 8
            #self.world_shift_y = 0
            player.speed = 0
        elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
            self.world_shift_x = -8
            #self.world_shift_y = 0
            player.speed = 0
        else:
            self.world_shift_x = 0
            #self.world_shift_y = 0
            player.speed = 8

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < screen_height / 4 and direction_y < 0:
            self.world_shift_y = 10
            player.jump_speed = 0
        elif player_y > screen_height - (screen_height / 3) and direction_y > 0:
            self.world_shift_y = -17
        else:
            self.world_shift_y = 0
            player.jump_speed = -16

    def world_shift(self):
        #self.scroll_y()
        self.scroll_x()

    def is_payer_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particles = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particles)

    def is_player_alive(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def has_player_won(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_platform_collision(self):
        #collided_platforms = pygame.sprite.spritecollide(self.player.sprite, self.moving_platform_sprites, False)

        for platform in self.moving_platform_sprites:
            if platform.rect.colliderect(self.player.sprite.collision_rect):
                self.player.sprite.rect.centerx += platform.speed

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.coin_sound.play()

    def check_enemy_collisions(self):
        # to achieve this we will check if the bottom of the player is in the top half of the enemy
        # and the player is going down, we know we are destroying the enemy
        # but if player has collided in any different way, he will take damage
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom

                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    self.stomp_sound.play()
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # run the entire game/level

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift_x, self.world_shift_y)

        # bg palms
        self.bg_palm_sprites.update(self.world_shift_x, self.world_shift_y)
        self.bg_palm_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift_x, self.world_shift_y)
        self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift_x, self.world_shift_y)
        self.terrain_sprites.draw(self.display_surface)

        # constraints
        self.constraint_sprites.update(self.world_shift_x, self.world_shift_y)

        # moving platform
        self.moving_platform_sprites.update(self.world_shift_x, self.world_shift_y)
        self.platform_collision_reverse()
        self.moving_platform_sprites.draw(self.display_surface)

        # enemies
        self.enemy_sprites.update(self.world_shift_x, self.world_shift_y)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift_x, self.world_shift_y)
        self.explosion_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift_x, self.world_shift_y)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift_x, self.world_shift_y)
        self.grass_sprites.draw(self.display_surface)

        # player sprites
        self.world_shift()
        self.player.update()
        self.check_platform_collision()
        self.horizontal_movement_collision()
        self.is_payer_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # fg palms
        self.fg_palm_sprites.update(self.world_shift_x, self.world_shift_y)
        self.fg_palm_sprites.draw(self.display_surface)

        # goal
        self.goal.update(self.world_shift_x, self.world_shift_y)
        self.goal.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift_x, self.world_shift_y)
        self.coin_sprites.draw(self.display_surface)

        self.is_player_alive()
        self.has_player_won()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface, self.world_shift_x, self.world_shift_y)
