import pygame
from sprites.platform import Platform, MovingPlatform
from sprites.flag import Flag
from sprites.enemy import Enemy
from sprites.coin import Coin
from settings import *

# Define 3 simple levels using lists of platform data
# Format: (x, y, w, h) for static, (x, y, w, h, dist, speed, dir) for moving
LEVEL_DATA = [
    # Level 1: Intro
    {
        "platforms": [
            (0, HEIGHT - 40, WIDTH * 2, 40), # Ground
            (300, HEIGHT - 150, 100, 20),
            (500, HEIGHT - 250, 100, 20),
            (700, HEIGHT - 350, 100, 20),
        ],
        "moving_platforms": [],
        "enemies": [
            (350, HEIGHT - 150, 40),
            (550, HEIGHT - 250, 40),
        ],
        "coins": [
            (350, HEIGHT - 180),
            (550, HEIGHT - 280),
            (750, HEIGHT - 380),
        ],
        "flag": (900, HEIGHT - 40)
    },
    # Level 2: Moving Platforms
    {
        "platforms": [
            (0, HEIGHT - 40, 400, 40), # Ground
            (800, HEIGHT - 40, 400, 40), # Ground 2
        ],
        "moving_platforms": [
            (450, HEIGHT - 150, 100, 20, 200, 2, "x"),
        ],
        "enemies": [
            (900, HEIGHT - 40, 100),
        ],
        "coins": [
            (450, HEIGHT - 180),
            (500, HEIGHT - 180),
            (550, HEIGHT - 180),
        ],
        "flag": (1100, HEIGHT - 40)
    },
    # Level 3: Parkour
    {
        "platforms": [
            (0, HEIGHT - 40, 200, 40),
            (250, HEIGHT - 150, 50, 20),
            (400, HEIGHT - 300, 50, 20),
            (550, HEIGHT - 450, 50, 20),
            (800, HEIGHT - 450, 300, 40)
        ],
        "moving_platforms": [
            (650, HEIGHT - 200, 50, 20, 300, 3, "y")
        ],
        "enemies": [
            (900, HEIGHT - 450, 100),
            (1000, HEIGHT - 450, 100),
        ],
        "coins": [
            (275, HEIGHT - 180),
            (425, HEIGHT - 330),
            (575, HEIGHT - 480),
        ],
        "flag": (1000, HEIGHT - 450)
    }
]

class Level:
    def __init__(self, game, level_idx):
        self.game = game
        self.level_idx = level_idx
        self.data = LEVEL_DATA[level_idx]
        
    def load(self):
        # Clear existing platforms and flag
        self.game.platforms.empty()
        self.game.enemies.empty()
        self.game.coins.empty()
        
        if hasattr(self.game, 'flag') and self.game.flag:
            self.game.flag.kill()
            
        # Load platforms
        for p in self.data["platforms"]:
            plat = Platform(*p)
            self.game.platforms.add(plat)
            self.game.all_sprites.add(plat)
            
        # Load moving platforms
        for mp in self.data["moving_platforms"]:
            plat = MovingPlatform(*mp)
            self.game.platforms.add(plat)
            self.game.all_sprites.add(plat)
            
        # Load enemies
        for e in self.data.get("enemies", []):
            enemy = Enemy(*e)
            self.game.enemies.add(enemy)
            self.game.all_sprites.add(enemy)
            
        # Load coins
        for c in self.data.get("coins", []):
            coin = Coin(*c)
            self.game.coins.add(coin)
            self.game.all_sprites.add(coin)
            
        # Load flag
        fx, fy = self.data["flag"]
        self.game.flag = Flag(fx, fy)
        self.game.all_sprites.add(self.game.flag)
