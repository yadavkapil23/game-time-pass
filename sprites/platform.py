import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=GREEN):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, dist, speed, dir="x", color=BROWN):
        super().__init__(x, y, w, h, color)
        self.start_x = x
        self.start_y = y
        self.dist = dist
        self.speed = speed
        self.dir = dir # "x" or "y"
        self.move_dir = 1
        
    def update(self):
        if self.dir == "x":
            self.rect.x += self.speed * self.move_dir
            if abs(self.rect.x - self.start_x) > self.dist:
                self.move_dir *= -1
        else:
            self.rect.y += self.speed * self.move_dir
            if abs(self.rect.y - self.start_y) > self.dist:
                self.move_dir *= -1
