import pygame
from config import *
from pygame.locals import *


class InvisiblePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA) 
        self.rect = self.image.get_rect(topleft=(x, y))