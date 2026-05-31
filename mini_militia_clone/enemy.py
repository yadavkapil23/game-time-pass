import pygame
import math
import random
from settings import *
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = self.pos
        
        self.speed = 2.0
        self.health = 50
        
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000 # 1 second between shots
        
    def update(self):
        # Very simple AI: fly towards player directly ignoring gravity for simplicity, or just hover
        target_x = self.game.player.rect.centerx
        target_y = self.game.player.rect.centery
        
        dx = target_x - self.pos.x
        dy = target_y - self.pos.y
        distance = math.hypot(dx, dy)
        
        # Move towards player if far, stay back if close
        if distance > 300:
            if distance != 0:
                self.pos.x += (dx / distance) * self.speed
                self.pos.y += (dy / distance) * self.speed
        
        self.rect.center = self.pos
        
        # Shoot at player if line of sight (simplified, just shoot if close enough)
        if distance < 500:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
                
    def shoot(self):
        # Slightly inaccurate shot
        target_x = self.game.player.rect.centerx + random.randint(-20, 20)
        target_y = self.game.player.rect.centery + random.randint(-20, 20)
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
        bullet.image.fill(ORANGE) # Enemy bullets are orange
        # We need a way to distinguish enemy bullets from player bullets for collision
        bullet.is_enemy = True
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)
