import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *
from random import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, positions, elementos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft= positions)
        self.elementos = elementos
        
        self.obstacles = pygame.sprite.Group()
        for idx, elemento in enumerate(self.elementos):
            obstacle = Obstacle(elemento, self.positions[idx])
        self.obstacles.add(obstacle)

