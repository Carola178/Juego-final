import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *


class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, posiciones, shoot_sound) -> None:
        super().__init__(groups)
        
        self.sheet_stars = SpriteSheets(pygame.image.load("./src/assets/images/yellowshot.png").convert_alpha(), 1, 8, 42, 50)
        self.animations_stars = self.sheet_stars.get_animation_stars()
        self.indice = 0
        self.image = self.animations_stars[self.indice]
        self.rect = self.image.get_rect(center = posiciones)
        self.speed = 5  # Velocidad de las estrellas hacia arriba
        self.shoot_sound = shoot_sound

        self.shoot_sound.play()
        
    def update(self):
# Mueve las estrellas hacia arriba
        self.rect.y -= self.speed
    # Elimina las estrellas cuando salen de la pantalla
        if self.rect.bottom < 0:
            self.kill()    
