import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.fuel = MAX_FUEL
        self.health = 100
        
    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        else:
            self.vel.x = 0
            
        # Jetpack flight
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.fuel > 0:
                self.acc.y = JETPACK_THRUST
                self.fuel -= FUEL_DRAIN
        else:
            # Regen handled below if grounded
            pass
            
        self.vel += self.acc
        
        # X Collision
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.centerx = self.pos.x
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if self.vel.x > 0:
                self.pos.x = hits[0].rect.left - self.rect.width / 2
            elif self.vel.x < 0:
                self.pos.x = hits[0].rect.right + self.rect.width / 2
            self.vel.x = 0
            self.rect.centerx = self.pos.x
            
        # Y Collision
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.centery = self.pos.y
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        is_grounded = False
        if hits:
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top - self.rect.height / 2
                is_grounded = True
            elif self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom + self.rect.height / 2
            self.vel.y = 0
            self.rect.centery = self.pos.y
            
        # Fuel regen
        if is_grounded and not (keys[pygame.K_w] or keys[pygame.K_SPACE]):
            self.fuel += FUEL_REGEN
            if self.fuel > MAX_FUEL:
                self.fuel = MAX_FUEL
