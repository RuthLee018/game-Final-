import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("images/p3.bmp")
        self.rect = self.image.get_rect()

        
        self.rect.x = self.screen_rect.width - self.rect.width
        self.rect.y = self.screen_rect.height - self.rect.height