import pygame
from settings import *
from arena import Block
from player import Player
from bullet import Bullet
from enemy import Enemy
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.state = "PLAYING"
        self.ui = UI(self)
        
        # Camera offset
        self.camera = pygame.math.Vector2(0, 0)
        
    def setup(self):
        self.all_sprites.empty()
        self.blocks.empty()
        self.bullets.empty()
        self.enemies.empty()
        
        # Build arena
        self.build_arena()
        
        # Spawn Player
        self.player = Player(self, 400, 300)
        self.all_sprites.add(self.player)
        
    def build_arena(self):
        # Very simple bounded arena
        # Borders
        for x in range(0, 2050, 50):
            b1 = Block(x, 0, 50, 50)
            b2 = Block(x, 1500, 50, 50)
            self.all_sprites.add(b1, b2)
            self.blocks.add(b1, b2)
        for y in range(0, 1550, 50):
            b1 = Block(0, y, 50, 50)
            b2 = Block(2000, y, 50, 50)
            self.all_sprites.add(b1, b2)
            self.blocks.add(b1, b2)
            
        # Some inner platforms
        platforms = [
            (300, 500, 300, 50),
            (800, 400, 200, 50),
            (500, 800, 400, 50),
            (1200, 600, 300, 50),
            (1000, 1000, 400, 50),
            (400, 1100, 200, 50)
        ]
        for p in platforms:
            b = Block(*p)
            self.all_sprites.add(b)
            self.blocks.add(b)
            
        # Spawn some enemies
        enemies_pos = [
            (500, 400),
            (900, 300),
            (600, 700),
            (1100, 500)
        ]
        for e in enemies_pos:
            enemy = Enemy(self, *e)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            
    def handle_event(self, event):
        if self.state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x = mouse_x + self.camera.x
                    world_y = mouse_y + self.camera.y
                    
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, world_x, world_y)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
        elif self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.setup()
                self.state = "PLAYING"
        
    def update(self):
        if self.state == "PLAYING":
            self.all_sprites.update()
            
            # Bullet collision with blocks
            pygame.sprite.groupcollide(self.bullets, self.blocks, True, False)
            
            # Bullet collision with entities
            for bullet in self.bullets:
                if not bullet.is_enemy:
                    hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
                    if hits:
                        bullet.kill()
                        hits[0].health -= 25
                        if hits[0].health <= 0:
                            hits[0].kill()
                else:
                    if pygame.sprite.collide_rect(bullet, self.player):
                        bullet.kill()
                        self.player.health -= 10
                        if self.player.health <= 0:
                            self.player.kill()
                            
            if not self.player.alive():
                self.state = "GAME_OVER"
            
            # Update Camera to follow player smoothly
            target_x = self.player.rect.centerx - WIDTH / 2
            target_y = self.player.rect.centery - HEIGHT / 2
            
            # Simple lerp
            self.camera.x += (target_x - self.camera.x) * 0.1
            self.camera.y += (target_y - self.camera.y) * 0.1
        
    def draw(self):
        if self.state == "PLAYING":
            # Draw all sprites with camera offset
            for sprite in self.all_sprites:
                rect = sprite.rect.move(-self.camera.x, -self.camera.y)
                self.screen.blit(sprite.image, rect)
                
        self.ui.draw()
