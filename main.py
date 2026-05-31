import pygame
import sys
from settings import *
from game import Game
def main():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init() # Initialize sound
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Platformer")
    
    clock = pygame.time.Clock()
    
    # Initialize game instance
    game = Game(screen)
    game.setup()
    
    # Main game loop
    running = True
    while running:
        # Keep loop running at the right speed
        clock.tick(FPS)
        
        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
            
        # Update
        game.update()
        
        # Draw / render
        screen.fill(SKY_BLUE)
        game.draw(screen)
        
        # *after* drawing everything, flip the display
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
