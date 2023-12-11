import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_sheets: SpriteSheets):
        super().__init__(groups)
        self.animations = sprite_sheets.get_animation_dict(scale=1)
        self.direction = "right"
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topright=(WIDTH, 0))
        self.speed = 1
        self.player = None
        self.last_fire_time = pygame.time.get_ticks()

    def update(self):
        self.animate()
        self.move_towards_player(self.player)        
        self.move()
        
        # Cambiar la imagen de acuerdo a la dirección
        if self.rect.x < self.player.rect.x:
            self.direction = "right"
        else:
            self.direction = "left"
            
        self.image = self.animations[self.direction][0]        

    def animate(self):
        self.image = self.animations[self.direction][0]
    
    def set_player(self, player):
        self.player = player
            
    def move(self):
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0

        if self.rect.bottom <= 0:
            self.rect.top = HEIGHT
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
            
    def move_towards_player(self, player):
        if self.player:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            
            if distance != 0:
                dx /= distance
                dy /= distance
            
            min_distance = 50
            
            if distance > min_distance:
                self.rect.x += self.speed * dx
                self.rect.y += self.speed * dy
