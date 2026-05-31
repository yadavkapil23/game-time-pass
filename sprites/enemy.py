import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_dist):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.start_x = x
        self.walk_dist = walk_dist
        self.speed = 1.5
        self.vel_x = self.speed
        
    def update(self):
        self.rect.x += self.vel_x
        if abs(self.rect.centerx - self.start_x) > self.walk_dist:
            self.vel_x *= -1
