import pygame

# Screen & Game
WIDTH = 800
HEIGHT = 600
FPS = 60
TILE_SIZE = 32
WORLD_WIDTH = 50  
WORLD_HEIGHT = 50

# Colors
COLORS = {
    "bg": (20, 20, 30),
    "floor": (40, 40, 50),
    "wall": (100, 100, 120),
    "text": (255, 255, 255),
    "player": (0, 200, 100),
    "npc": (200, 200, 0),
    "chest": (200, 150, 50),
    "ui_bg": (10, 10, 18, 200)
}

# Player Stats
PLAYER_WALK_SPEED = 150
PLAYER_RUN_SPEED = 250
PLAYER_ANIMATION_TIME = 0.15

# Keys
KEY_BINDINGS = {
    "menu": pygame.K_ESCAPE,
    "confirm": pygame.K_RETURN,
    "back": pygame.K_BACKSPACE,
    "interact": pygame.K_e
}