"""The level.py module contains the Level class,
which is responsible for managing the game logic, rendering, and interactions within individual levels of the game.
"""

import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm, Spikes, RumBottle, Treasure
from enemy import Enemy
from shell_enemy import Shell
from boss import Boss
from moving_platform import MovingPlatform
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    """The Level class represents an individual level in the game. It handles the setup,
        updating, and rendering of various game elements such as terrain, player, enemies, collectibles, and more.

        Parameters:
                current_level: The current level number.
                surface: The Pygame surface object representing the game window.
                create_overworld: Callback function to create the overworld when transitioning between levels.
                change_coins: Callback function to change the number of coins collected.
                change_health: Callback function to change the player's health.
    """
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):

        # general setup
        self.display_surface = surface
        self.world_shift_x = 0

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

        # health setup
        health_layout = import_csv_layout(level_data['health'])
        self.health_sprites = self.create_tile_group(health_layout, 'health')

        # coins setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coins_layout, 'coins')

        # foreground palms setup
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # background palms setup
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # spikes setup
        spikes_layout = import_csv_layout(level_data['spikes'])
        self.spike_sprites = self.create_tile_group(spikes_layout, 'spikes')

        # enemy setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # shell setup
        shell_layout = import_csv_layout(level_data['shell'])
        self.shell_sprites = self.create_tile_group(shell_layout, 'shell')
        self.pearl_sprite = pygame.sprite.Group()

        # boss setup
        boss_layout = import_csv_layout(level_data['boss'])
        self.boss_sprite = self.create_tile_group(boss_layout, 'boss')

        # treasure setup
        treasure_layout = import_csv_layout(level_data['treasure'])
        self.treasure_sprite = self.create_tile_group(treasure_layout, 'treasure')

        # enemy constraint setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # decoration
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        """Creates a sprite group for a specific type of tile based on layout data, imported from the corresponding
            .csv file in the level_data dictionary.

            Parameters:
                layout: Layout data parsed from CSV files.
                type: Type of tile group to create (e.g., terrain, moving platform, crates).

            Returns: Sprite group containing tiles of the specified type.
        """
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
                        if val == '0':
                            sprite = MovingPlatform(tile_size, x, y, '../graphics/terrain/moving_platforms/horizontal_platform.png',
                                                    'horizontal')
                        elif val == '1':
                            sprite = MovingPlatform(tile_size, x, y, '../graphics/terrain/moving_platforms/small_island_horiz.png',
                                                    'horizontal')
                        elif val == '2':
                            sprite = MovingPlatform(tile_size, x, y, '../graphics/terrain/moving_platforms/small_island_vert.png',
                                                    'vertical')
                        else:
                            sprite = MovingPlatform(tile_size, x, y, '../graphics/terrain/moving_platforms/vertical_platform.png',
                                                    'vertical')

                    elif type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    elif type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    elif type == 'health':
                        sprite = RumBottle(tile_size, x, y)

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

                    elif type == 'spikes':
                        sprite = Spikes(tile_size, x, y)

                    elif type == 'treasure':
                        sprite = Treasure(tile_size, x, y)

                    elif type == 'enemies':
                        sprite = Enemy(tile_size, x, y,)

                    elif type == 'shell':
                        if val == '0':
                            sprite = Shell(tile_size, x, y, 'left')
                        elif val == '1':
                            sprite = Shell(tile_size, x, y, 'right')

                    elif type == 'boss':
                        sprite = Boss(tile_size * 3, x, y)

                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        """ Sets up the player sprite based on layout data.

            Parameters:
                layout: Layout data parsed from CSV files.
                change_health: Callback function to change the player's health.
        """
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
        """This method handles reversing the movement direction of moving platforms
            when they collide with invisible to the player constraint tiles.
        """
        for platform in self.moving_platform_sprites:
            if pygame.sprite.spritecollide(platform, self.constraint_sprites, False):
                platform.reverse()

    def enemy_collision_reverse(self):
        """Handles reversing the movement direction of enemies
            when they collide with invisible to the player constraint tiles.
        """
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        """Generates jump particles when the player jumps or lands, adding visual effects to enhance gameplay."""
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
        """Handles horizontal movement collision detection for the player.
            The method is called during each game update cycle and is responsible for ensuring
            that the player sprite does not move through solid objects horizontally.
            It adjusts the player's collision rectangle (collision_rect) based on its movement direction and speed.
            It iterates over all collidable_sprites (terrain, crates, moving platforms, shells.)
            to check for collisions with the player's collision rectangle using the colliderect method.

            If a collision is detected:
                If the player is moving left (direction.x < 0), it positions the player's collision rectangle
                to the right of the collided object, setting the players on_left state to True
                and prevents further movement left.

                If the player is moving right (direction.x > 0), it positions the player's collision rectangle
                to the left of the collided object, setting the players on_right state to True
                and prevents further movement right.
        """
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = (self.terrain_sprites.sprites() + self.crate_sprites.sprites() +
                              self.moving_platform_sprites.sprites() + self.shell_sprites.sprites())

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
        """ Handles vertical movement collision detection for the player.
            The method is called during each game update cycle and prevents the player sprite
            from falling through solid objects (ground) and from passing through ceilings.
            It adjusts the player's collision rectangle (collision_rect) based on its movement direction and speed.
            It iterates hover all collidable_sprites (terrain, crates, moving platforms, shells)
            to check for collisions with the player's collision rectangle using the colliderect method.

            If a collision is detected:
                If the player is moving downward (direction.y > 0), it positions the player's collision rectangle
                above the collided object and sets the payers state on_ground to True,
                preventing further downward movement.

                If the player is moving upward (direction.y < 0), it positions the player's collision rectangle
                below the collided object and sets the payers state on_ceiling to True,
                preventing further upward movement.

                It also handles special cases like landing on moving platforms,
                by passing a reference to the exact moving platform with which a collision has occured,
                to the players on_platform attribute.

                If the players state on_ground is True and he is moving upward or downward
                the players on_ground state must be reverted to False and his on_platform attribute set to Null.
        """
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = (self.terrain_sprites.sprites() + self.crate_sprites.sprites() +
                              self.moving_platform_sprites.sprites() + self.shell_sprites.sprites())

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if isinstance(sprite, MovingPlatform):
                    player.on_platform = sprite
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
                player.on_platform = None

    def scroll_x(self):
        """Scrolls the game world horizontally based on player movement.
            When the player reaches a certain portion of the screen, his movement speed is set to 0
            and teh screen/camera starts shifting in the current direction at the same speed.
        """
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 2.7 and direction_x < 0:
            self.world_shift_x = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2.7) and direction_x > 0:
            self.world_shift_x = -8
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 8

    def world_shift(self):
        """Updates the world shift based on player movement."""
        self.scroll_x()

    def is_payer_on_ground(self):
        """Sets the player status on_ground to True or False, depending on collision.
            Important for the vertical_movement_collision and whether the gravity/falling will be applied to the palyer.
        """
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        """Creates dust particles upon landing."""
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particles = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particles)

    def is_player_alive(self):
        """Checks if the player has fallen of the screen."""
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def has_player_won(self):
        """Checks if the player has won the level and unlocks the next one."""
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_bottle_collisions(self):
        """Checks for collisions between the player and health items and heals the player."""
        for bottle in self.health_sprites:
            if bottle.rect.colliderect(self.player.sprite.collision_rect):
                bottle.kill()
                self.player.sprite.heal()
                self.coin_sound.play()

    def check_coin_collisions(self):
        """Checks for collisions between the player and coins and updates the current coin value."""
        for coin in self.coin_sprites:
            if coin.rect.colliderect(self.player.sprite.collision_rect):
                coin.kill()
                self.change_coins(coin.value)
                self.coin_sound.play()

    def check_for_shell_sight(self):
        """Checks if the player is within the sight range of shell enemies.
            If the player is within this range (x and y respectively),
            the shell enemy calls its shoot method and adds a pearl to the pearl_sprite group.
        """
        for shell in self.shell_sprites:
            if shell.direction == 'left':
                sight_range_start = shell.rect.x - 7 * tile_size
                sight_range_end = shell.rect.x
            else:
                sight_range_start = shell.rect.x
                sight_range_end = shell.rect.x + 7 * tile_size

            if sight_range_start <= self.player.sprite.collision_rect.x <= sight_range_end\
                    and self.player.sprite.collision_rect.y == (shell.rect.y - 10):
                shell.shoot()
                self.pearl_sprite.add(shell.pearl)
            else:
                shell.frames = shell.idle_frames

    def check_boss_sight(self):
        """ Checks if the player is within sight range of the boss enemy.
            If in range, the boss will move in the players direction, and if not in sight
            the boss stops in the same place.
        """
        player = self.player.sprite
        boss_sprites = self.boss_sprite.sprites()

        if boss_sprites:
            boss = boss_sprites[0]
            left_sight_range = boss.rect.x - (15 * tile_size)
            right_sight_range = boss.rect.x + (15 * tile_size)

            if left_sight_range <= player.rect.x <= boss.rect.x and boss.is_target_in_height_range(player.rect.y):
                boss.move_left()
            elif right_sight_range >= player.rect.x >= boss.rect.x and boss.is_target_in_height_range(player.rect.y):
                boss.move_right()
            else:
                boss.stop()

    def check_pearl_collision(self):
        """Checks for collisions between the player and pearls and player takes damage."""
        for pearl in self.pearl_sprite:
            if pearl.rect.colliderect(self.player.sprite.collision_rect):
                pearl.has_hit = True
                self.player.sprite.get_damage(-10)

    def check_spike_collision(self):
        """Checks for collisions between the player, boss and spikes.
            Both the boss and player take damage from the spikes.
        """
        boss_sprites = self.boss_sprite.sprites()
        for spikes in self.spike_sprites:
            if spikes.rect.colliderect(self.player.sprite.collision_rect):
                self.player.sprite.get_damage(-10)
                self.player.sprite.direction.y = - 15
            elif boss_sprites:
                boss = boss_sprites[0]
                if spikes.rect.colliderect(boss.rect):
                    boss.take_damage()
                    if not boss.is_alive():
                        explosion_sprite = ParticleEffect(boss.rect.center, 'explosion')
                        self.explosion_sprites.add(explosion_sprite)
                        self.stomp_sound.play()
                        boss.kill()
                        self.change_coins(500)

    def check_enemy_collisions(self):
        # to achieve this we will check if the bottom of the player is in the top half of the enemy
        # and the player is going down, we know we are destroying the enemy
        # but if player has collided in any different way, he will take damage

        """ Checks for collisions between the player and enemies/boss.
            Depending on the te collision, the player will kill the enemy of his bottom collides
            with the top of the enemy sprite. Any other collision will result in the player taking damage.

            The boss cannot be killed by the player directly, so any type of collision with him,
            will result in the player taking damage equal to one third of his total health.
        """
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        boss_collision = pygame.sprite.spritecollide(self.player.sprite, self.boss_sprite, False)

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
                    self.player.sprite.get_damage(-10)

        elif boss_collision:
            self.player.sprite.get_damage(-34)
            self.player.sprite.direction.y = -15

    def run(self):
        """ Runs the entire level, including updating and rendering game elements,
            handling interactions, and triggering events.
        """

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift_x)

        # bg palms
        self.bg_palm_sprites.update(self.world_shift_x)
        self.bg_palm_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift_x)
        self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift_x)
        self.terrain_sprites.draw(self.display_surface)

        # constraints
        self.constraint_sprites.update(self.world_shift_x)

        # moving platform
        self.moving_platform_sprites.update(self.world_shift_x)
        self.platform_collision_reverse()
        self.moving_platform_sprites.draw(self.display_surface)

        # enemies
        self.enemy_sprites.update(self.world_shift_x)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift_x)
        self.explosion_sprites.draw(self.display_surface)

        # shells
        self.shell_sprites.update(self.world_shift_x)
        self.shell_sprites.draw(self.display_surface)

        # pearl
        self.pearl_sprite.update(self.world_shift_x, surface=self.display_surface)
        self.pearl_sprite.draw(self.display_surface)

        #boss
        self.boss_sprite.update(self.world_shift_x)
        self.boss_sprite.draw(self.display_surface)

        # spikes
        self.spike_sprites.update(self.world_shift_x)
        self.check_spike_collision()
        self.spike_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift_x)
        self.crate_sprites.draw(self.display_surface)

        # health
        self.health_sprites.update(self.world_shift_x)
        self.health_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift_x)
        self.grass_sprites.draw(self.display_surface)

        # player sprites
        self.world_shift()
        self.player.update()
        self.horizontal_movement_collision()
        self.is_payer_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # fg palms
        self.fg_palm_sprites.update(self.world_shift_x)
        self.fg_palm_sprites.draw(self.display_surface)

        # goal
        self.goal.update(self.world_shift_x)
        self.goal.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift_x)
        self.coin_sprites.draw(self.display_surface)

        # treasure chest
        self.treasure_sprite.update(self.world_shift_x)
        self.treasure_sprite.draw(self.display_surface)

        self.is_player_alive()
        self.has_player_won()

        self.check_bottle_collisions()
        self.check_coin_collisions()
        self.check_boss_sight()
        self.check_for_shell_sight()
        self.check_pearl_collision()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface, self.world_shift_x)
