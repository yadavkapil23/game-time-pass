import pygame
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        # Make it circular
        pygame.draw.circle(self.image, YELLOW, (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
