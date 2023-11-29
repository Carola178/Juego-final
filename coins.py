import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *
from random import *
from player import Player


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size=(WIDTH_PLAYER, HEIGHT_PLAYER)):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


