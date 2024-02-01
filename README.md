## 1. Introduction

Welcome to the Quest For Booty Game! This documentation provides an overview of the game, features, controls, installation instructions, and other relevant information.

## 2. Game Overview

Quest For Booty is a classic platformer where players navigate through levels, collect coins and overcome challenges.

## 3. Features

- Multiple levels with increasing difficulty.
- Health system and coin collection mechanics.
- Overworld and level transitions.
- Moving platforms
- Mele and ranged enemy types
- User Interface (UI) elements for health and coin display.
- Animations

## 4. Controls

The game uses the keyboard for controls. Very simple platformer control scheme:
'A' button - Move left
'D' button - Move right
'Spacebar' - Jump

Choosing a level from the Overworld:
'Left arrow key' - move select icon left
'Right arrow key' - move select icon right
'Spacebar' - select level 

## 5. Installation

1. Clone the repository.
2. Install the required dependencies, including Pygame.
3. Run `main.py` to start the game.

## 6. How to Play

Navigate through the overworld and levels using the provided controls. Collect coins to increase your score and avoid obstacles and enemies. 
The game features a health system, and reaching zero health resets the game.

# 7. Code Structure

The Quest For Booty project is organized into several files, each responsible for specific aspects of the game. Let's delve into the details of each file:

## `main.py`

- **Description:**
  - Contains the main game logic, flow control, and entry point for the game.

- **Key Components:**
  - `Game` class: Manages game attributes, audio, overworld, level creation, UI, and game flow.
  - `create_overworld`: Handles level transitions and updates the overworld.

## `player.py`

- **Description:**
  - Implements the player character.

- **Key Components:**
  - `Player` class: Represents the player character with movement, jumping, and health mechanics.

## `level.py`

- **Description:**
  - Manages level creation, including terrain, moving platforms, enemies, coins, and more.

- **Key Components:**
  - `Level` class: Handles level setup, player initialization, and collision detection.
  - `MovingPlatform` class: Represents moving platforms in the game.
  - `Enemy` class: Represents various enemy types.
  - `Shell` class: Represents an enemy that shoots projectiles.
  - `Boss` class: Represents a boss enemy with unique mechanics.

## `tiles.py`

- **Description:**
  - Defines tile classes used for terrain and decorations.

- **Key Components:**
  - `Tile`, `StaticTile`, `Crate`, `Coin`, `Palm`, `Spikes`, `RumBottle`, `Treasure`: Different types of tiles.
  - `AnimatedTile` class: Base class for tiles with animations.

## `ui.py`

- **Description:**
  - Manages UI elements such as health bars and coin displays.

- **Key Components:**
  - `UI` class: Handles UI setup and rendering.

## `decorations.py`

- **Description:**
  - Manages decorative elements like the sky, water, clouds, and particle effects.

- **Key Components:**
  - `Sky`, `Water`, `Clouds` classes: Represent different decorative elements.

## `boss.py`

- **Description:**
  - Implements the boss enemy with unique mechanics.

- **Key Components:**
  - `Boss` class: Represents the boss enemy with movement, damage, and invincibility mechanics.

## `shell_enemy.py`

- **Description:**
  - Defines a shell enemy that shoots projectiles.

- **Key Components:**
  - `Shell` class: Represents the shell enemy with movement and projectile shooting mechanics.

## `enemy.py`

- **Description:**
  - Implements various enemy types.

- **Key Components:**
  - `Enemy` class: Represents different enemy types with movement and behavior.

## `moving_platform.py`

- **Description:**
  - Defines moving platforms with different movement patterns.

- **Key Components:**
  - `MovingPlatform` class: Represents moving platforms with horizontal and vertical movement.

## `support.py`

- **Description:**
  - Provides utility functions for importing graphics and CSV layout files.

- **Key Functions:**
  - `import_folder`, `import_csv_layout`, `import_cut_graphics`: Functions for loading images and CSV layouts.

## Game Flow:

1. **Initialization:**
   - `main.py` initializes the game, sets up Pygame, and manages the overall game flow.

2. **Player Controls:**
   - Player character in `player.py` is controlled using keyboard inputs (`A`, `D`, `Spacebar`).

3. **Level Creation:**
   - `level.py` handles level creation, including terrain, enemies, and other elements.

4. **Collision Detection:**
   - Collision detection is implemented in the `Level` class for various interactions, such as player-enemy collisions, coin collection, and more.

5. **Health System and UI:**
   - The game features a health system, and the UI is managed by the `ui.py` file.

6. **Decorative Elements:**
   - Decorative elements, such as the sky and water, are managed by the `decorations.py` file.

7. **Boss Enemy:**
   - The boss enemy and its unique mechanics are implemented in the `boss.py` file.

8. **Other Enemies:**
   - Various enemy types, including shells, are implemented in `enemy.py` and `shell_enemy.py`.

9. **Moving Platforms:**
   - Different types of moving platforms are implemented in `moving_platform.py`.

10. **Utility Functions:**
   - `support.py` provides utility functions for loading graphics and CSV layout files.


## 8. Assets
The game uses several PNGs and images, located in the "graphics" folder, which contains subfolders corresponding with different parts and NPCs of the game, 
and a couple of audio files that are located in the "audio" folder, which are again divided into subfolders for the different types of sound effects.

## 9. Known Issues
Currently, there is a bug, where during the camera shifting, if a collision occurs between the player and a terrain tile, the player sprite will be moved to the top of the tile or a different type of movement glitch.

## 10. Credits
Game developed by: Nikolay Georgiev.
Pygame library: [https://www.pygame.org/news].
Most assets and base game logic from: [https://www.youtube.com/playlist?list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh-]

