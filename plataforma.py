import pygame
from config import *
from pygame.locals import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, groups, rect : pygame.Rect) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((rect[2], rect[3]))
        self.rect = self.image.get_rect(topleft = (rect[0], rect[1]))
        self.image.fill(black)