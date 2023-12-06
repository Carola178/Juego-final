import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *
from fire_dragon import Fire
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_sheets: SpriteSheets):
        super().__init__(groups)
        self.animations = sprite_sheets.get_animation_dict(scale=2)
        self.direction = "right"
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=(500, 300))
        self.speed = 3.5
        self.all_sprites = groups[0]
        self.shoot_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_bola_fuego.mp3")
        self.fire_rate = 2000  # Fuego cada 2 segundos (en milisegundos)
        self.last_fire_time = pygame.time.get_ticks()
        self.fires_group = pygame.sprite.Group()

    def update(self):
        self.animate()
        self.move()
        self.shoot_fire()

    def animate(self):
        # Lógica de animación basada en la dirección
        self.image = self.animations[self.direction][0]  # Aquí debes cambiar el índice de la animación actual

    def move(self):
        # Lógica para el movimiento del enemigo
        if self.direction == "right" and self.rect.right <= WIDTH:
            self.rect.x += self.speed
        elif self.direction == "right" and self.rect.right > WIDTH:
            self.direction = "left"
        elif self.direction == "left" and self.rect.left >= 0:
            self.rect.x -= self.speed
        elif self.direction == "left" and self.rect.left < 0:
            self.direction = "right"

    def shoot_fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time >= self.fire_rate:
            new_fire = Fire([self.all_sprites], self.rect.midtop, self.shoot_sound)
            self.all_sprites.add(new_fire)
            self.fires_group.add(new_fire)
            self.last_fire_time = current_time
