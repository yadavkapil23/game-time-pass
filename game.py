import pygame
from settings import *
from sprites.player import Player
from sprites.platform import Platform, MovingPlatform
from level import Level
from ui.ui import UI


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # We will initialize levels and states here later
        self.state = "PLAYING" # "START", "PLAYING", "GAME_OVER", "VICTORY"
        self.player = None
        self.current_level_idx = 0
        self.score = 0
        self.lives = 3
        
        # UI
        self.ui = UI(self)
        
        # This will hold the camera offset
        self.camera_x = 0
        
    def setup(self):
        """Initializes the game state and creates objects"""
        self.all_sprites.empty()
        self.platforms.empty()
        self.camera_x = 0
        
        # Load Level
        self.level = Level(self, self.current_level_idx)
        self.level.load()
        
        # Spawn player
        self.player = Player(self, WIDTH // 4, HEIGHT // 2) # Spawn more left
        self.all_sprites.add(self.player)
        
    def handle_event(self, event):
        """Handles pygame events"""
        if event.type == pygame.KEYDOWN:
            if self.state == "PLAYING":
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.player:
                        self.player.jump()
            elif self.state in ["GAME_OVER", "VICTORY"]:
                if event.key == pygame.K_r:
                    self.reset_game()
                    
    def reset_game(self):
        self.current_level_idx = 0
        self.score = 0
        self.lives = 3
        self.state = "PLAYING"
        self.setup()
                
    def update(self):
        """Updates game logic and sprites"""
        if self.state == "PLAYING":
            self.all_sprites.update()
            
            # Check death (fall off)
            if self.player.rect.top > HEIGHT:
                self.player.kill()
                self.setup() # Restart level for now
            
            # Check level completion
            if hasattr(self, 'flag') and pygame.sprite.collide_rect(self.player, self.flag):
                self.current_level_idx += 1
                if self.current_level_idx >= len(__import__('level').LEVEL_DATA):
                    self.state = "VICTORY"
                else:
                    self.setup() # Load next level
            
            # Coin Collision
            hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            for hit in hits:
                self.score += 10
                
            # Enemy Collision
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                # If player is falling and above the enemy's center, bounce and kill
                if self.player.vel.y > 0 and self.player.rect.bottom < hits[0].rect.centery:
                    self.player.vel.y = -8 # Bounce
                    hits[0].kill()
                    self.score += 50
                else:
                    # Player dies
                    self.player.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = "GAME_OVER"
                    else:
                        self.setup()
            
            # Simple Camera System
            scroll_margin = 300
            if self.player.rect.right > WIDTH - scroll_margin:
                shift = self.player.vel.x
                if shift > 0:
                    self.player.pos.x -= shift
                    self.camera_x += shift
                    for plat in self.platforms:
                        plat.rect.x -= shift
                        if hasattr(plat, 'start_x'):
                            plat.start_x -= shift
                    for enemy in self.enemies:
                        enemy.rect.x -= shift
                        if hasattr(enemy, 'start_x'):
                            enemy.start_x -= shift
                    for coin in self.coins:
                        coin.rect.x -= shift
                    if hasattr(self, 'flag'):
                        self.flag.rect.x -= shift
                            
            elif self.player.rect.left < scroll_margin:
                shift = self.player.vel.x
                if shift < 0 and self.camera_x > 0:
                    actual_shift = min(-shift, self.camera_x)
                    self.player.pos.x += actual_shift
                    self.camera_x -= actual_shift
                    for plat in self.platforms:
                        plat.rect.x += actual_shift
                        if hasattr(plat, 'start_x'):
                            plat.start_x += actual_shift
                    for enemy in self.enemies:
                        enemy.rect.x += actual_shift
                        if hasattr(enemy, 'start_x'):
                            enemy.start_x += actual_shift
                    for coin in self.coins:
                        coin.rect.x += actual_shift
                    if hasattr(self, 'flag'):
                        self.flag.rect.x += actual_shift
            
    def draw(self, screen):
        """Draws everything to the screen"""
        if self.state == "PLAYING":
            self.all_sprites.draw(screen)
            
        # Draw UI on top
        self.ui.draw()
