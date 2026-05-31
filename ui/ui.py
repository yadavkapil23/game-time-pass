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
        
    def draw(self):
        if self.game.state == "PLAYING":
            self.draw_text(f"Score: {self.game.score}", "normal", BLACK, 10, 10)
            self.draw_text(f"Lives: {self.game.lives}", "normal", BLACK, 10, 40)
            self.draw_text(f"Level: {self.game.current_level_idx + 1}", "normal", BLACK, WIDTH - 100, 10)
            
        elif self.game.state == "GAME_OVER":
            self.draw_text("GAME OVER", "large", RED, WIDTH // 2, HEIGHT // 2 - 50, "center")
            self.draw_text("Press 'R' to Restart", "normal", BLACK, WIDTH // 2, HEIGHT // 2 + 50, "center")
            
        elif self.game.state == "VICTORY":
            self.draw_text("VICTORY!", "large", GREEN, WIDTH // 2, HEIGHT // 2 - 50, "center")
            self.draw_text(f"Final Score: {self.game.score}", "normal", BLACK, WIDTH // 2, HEIGHT // 2 + 20, "center")
            self.draw_text("Press 'R' to Play Again", "normal", BLACK, WIDTH // 2, HEIGHT // 2 + 60, "center")
