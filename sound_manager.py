import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        # Example of loading a sound if the file exists
        # self.load_sound('jump', 'assets/sounds/jump.wav')
        # self.load_sound('coin', 'assets/sounds/coin.wav')
        
    def load_sound(self, name, path):
        if os.path.exists(path):
            self.sounds[name] = pygame.mixer.Sound(path)
        else:
            self.sounds[name] = None
            
    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
