import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *


class Fire(pygame.sprite.Sprite):
    def __init__(self, groups, posiciones, shoot_sound) -> None:
        super().__init__(groups)       
        self.sheet_fire = SpriteSheets(pygame.image.load("./src/assets/images/fire-dragon.png").convert_alpha(), 3, 3, 16, 16)
        self.animations_fire = self.sheet_fire.get_animation_stars()
        self.indice = 0
        self.image = self.animations_fire[self.indice]
        self.rect = self.image.get_rect(center = posiciones)
        self.speed = 4
        self.shoot_sound = shoot_sound

        self.shoot_sound.play()
        
    def update(self):
        self.rect.x -= self.speed
    
