import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_enemy = False
        
        self.speed = 15
        
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        
        if distance == 0:
            self.vel_x = self.speed
            self.vel_y = 0
        else:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
            
        self.pos = pygame.math.Vector2(x, y)
        
    def update(self):
        self.pos.x += self.vel_x
        self.pos.y += self.vel_y
        self.rect.center = self.pos
