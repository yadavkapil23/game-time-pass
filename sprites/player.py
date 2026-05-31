import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # Position and physics
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        # Jump logic
        self.jumps_left = 2 # Allow double jump
        
    def jump(self):
        # Allow jumping if standing on something or if double jump is available
        if self.jumps_left > 0:
            self.vel.y = PLAYER_JUMP
            self.jumps_left -= 1
            
    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
            
        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Equations of motion
        self.vel += self.acc
        
        # Limit very small velocities to 0 to prevent sliding
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
            
        # --- X Collision ---
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.midbottom = self.pos
        
        # Check collision with platforms (requires self.game.platforms to exist)
        if hasattr(self.game, 'platforms'):
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                if self.vel.x > 0: # moving right
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                elif self.vel.x < 0: # moving left
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.midbottom = self.pos
        
        # --- Y Collision ---
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos
        
        if hasattr(self.game, 'platforms'):
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                if self.vel.y > 0: # falling
                    self.pos.y = hits[0].rect.top
                    self.vel.y = 0
                    self.jumps_left = 2 # Reset jumps on landing
                    
                    # Moving platform interaction (X-axis)
                    if hasattr(hits[0], 'dir') and hits[0].dir == "x":
                        self.pos.x += hits[0].speed * hits[0].move_dir
                        
                elif self.vel.y < 0: # jumping and hitting head
                    self.pos.y = hits[0].rect.bottom + self.rect.height
                    self.vel.y = 0
                self.rect.midbottom = self.pos
