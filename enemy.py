import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_sheets: SpriteSheets):
        super().__init__(groups)
        self.animations = sprite_sheets.get_animation_dict(scale=2)
        self.directions = ["right", "left", "front", "back"]
        self.direction = "right"  # Dirección inicial
        self.current_sprite = 0
        self.image = self.animations[self.direction][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(500, 300))
        self.speed = 3.5
        self.last_update = pygame.time.get_ticks()
        self.time_animation = 100
        self.change_direction_interval = 4500  
        self.last_direction_change = pygame.time.get_ticks()
        self.stars_group = pygame.sprite.Group() 

    def update(self):
        self.move()

    def move(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.time_animation:
            self.current_sprite = (self.current_sprite + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.current_sprite]
            self.last_update = current_time

        # Control de movimiento horizontal dentro de los límites de la pantalla
        if self.direction == "right" and self.rect.right <= WIDTH:
            self.rect.x += self.speed
        elif self.direction == "left" and self.rect.left >= 0:
            self.rect.x -= self.speed

        # Verificar si es momento de cambiar de dirección
        if current_time - self.last_direction_change >= self.change_direction_interval:
            self.last_direction_change = current_time  # Actualizar el tiempo del último cambio de dirección
            if self.direction == "right":
                self.direction = "left"
            else:
                self.direction = "right"
