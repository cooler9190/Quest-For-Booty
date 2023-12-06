import pygame
from support import import_csv_layout, import_cut_graphics, import_folder
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

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

                    elif type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    elif type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    elif type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/gold')
                        else:
                            sprite = Coin(tile_size, x, y, '../graphics/coins/silver')

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

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                elif val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

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
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            # We use colliderect instead of sprite collision because we want to have access to each of the tile's rect
            # and with spritecollide would be a bit more difficult
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    # if direction is left we move the player exactly on the right of the collided object
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    # if direction is right we move the player exactly on the left of the collided object
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

            # direction.x is not reliable to tell if we stopped colliding with a wall, for example if we have jumped over it
            # instead, we record the x position of the collision and once the player has exceeded that position
            # (positively for right and negatively for left movement) we know the collision is false
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    # Once we hit a tile we reset the gravity to 0, so that it doesn't build up and destroy the player
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    # When we jump and hit a tile, we must reset the negative y, so that it doesn't increase
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

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

    def run(self):
        # run the entire game/level

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # bg palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemies and constraints
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # fg palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.is_payer_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
