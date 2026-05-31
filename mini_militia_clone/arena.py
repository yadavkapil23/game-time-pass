import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(LIGHT_GREY)
        pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 2) # border
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
