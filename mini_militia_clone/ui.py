import pygame
from settings import *

class UI:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 24)
        self.large_font = pygame.font.SysFont('arial', 64)
        
    def draw_text(self, text, size, color, x, y, align="topleft"):
        font = self.large_font if size == "large" else self.font
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if align == "center":
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)
        
    def draw_bar(self, x, y, width, height, pct, bg_color, fg_color):
        pct = max(0, min(1, pct))
        bg_rect = pygame.Rect(x, y, width, height)
        fg_rect = pygame.Rect(x, y, width * pct, height)
        pygame.draw.rect(self.screen, bg_color, bg_rect)
        pygame.draw.rect(self.screen, fg_color, fg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
    def draw(self):
        if getattr(self.game, 'state', 'PLAYING') == "PLAYING":
            # Player Health
            health_pct = self.game.player.health / 100.0 if self.game.player.alive() else 0
            self.draw_text("Health", "normal", WHITE, 20, 20)
            self.draw_bar(100, 25, 200, 20, health_pct, RED, GREEN)
            
            # Player Fuel
            fuel_pct = self.game.player.fuel / MAX_FUEL if self.game.player.alive() else 0
            self.draw_text("Fuel", "normal", WHITE, 20, 50)
            self.draw_bar(100, 55, 200, 20, fuel_pct, DARK_GREY, YELLOW)
            
        elif self.game.state == "GAME_OVER":
            self.draw_text("GAME OVER", "large", RED, WIDTH // 2, HEIGHT // 2 - 50, "center")
            self.draw_text("Press 'R' to Restart", "normal", WHITE, WIDTH // 2, HEIGHT // 2 + 50, "center")
