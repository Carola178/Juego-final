import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_sheets: SpriteSheets):
        super().__init__(groups)
        self.animations = sprite_sheets.get_animation_dict(scale = 2)
        self.directions = ["right", "left", "front", "back"]
        self.direction = "front"  # Dirección inicial
        self.current_sprite = 0
        self.image = self.animations[self.direction][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(70, 90))
        self.speed = 5.5
        self.last_update = pygame.time.get_ticks()
        self.time_animation = 100
        self.speed_vert = 0
        self.obstacles_group = None
        self.colliding = False
        self.image = pygame.Surface((30, 30))
        self.slow_speed = 2
        self.collision_duration = 1000 
        self.score = 0

    def set_obstacles_group(self, obstacles_group):
        self.obstacles_group = obstacles_group
        
    def update(self):
        self.handle_collision()
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if keys[K_RIGHT]:
            self.direction = "right"
            self.move(current_time)

        if keys[K_LEFT]:
            self.direction = "left"
            self.move(current_time)


        if keys[K_DOWN]:
            self.direction = "front"
            self.move(current_time)


        if keys[K_UP]:
            self.direction = "back"
            self.move(current_time)
            
        self.speed_vert += GRAVEDAD
        self.rect.y += self.speed_vert
        
        # Restricciones del suelo
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_vert = 0
            
        # Actualización de la animación
        self.update_animation(current_time)            
        
        super().update()        
        
    def handle_collision(self):
        collisions = pygame.sprite.spritecollide(self, self.obstacles_group, False)
        if collisions:
            self.score -= 10  
            if self.score < 0:
                self.score = 0 
        
    def update_animation(self, current_time):
        # Actualizar la animación del jugador
        if current_time - self.last_update >= self.time_animation:
            self.current_sprite = (self.current_sprite + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.current_sprite]
            self.last_update = current_time
        
                
    def move(self, current_time):
        if current_time - self.last_update >= self.time_animation:
            self.current_sprite = (self.current_sprite + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.current_sprite]
            self.last_update = current_time
        
        if self.direction == "right" and self.rect.right <= WIDTH:
            self.rect.x += self.speed
        elif self.direction == "left" and self.rect.left >= 0:
            self.rect.x -= self.speed
        elif self.direction == "front" and self.rect.bottom <= HEIGHT:
            self.rect.y += self.speed
        elif self.direction == "back" and self.rect.top >= 0:
            self.rect.y -= self.speed
            
    def jump(self):
        self.speed_vert = -25
        
    def reset_position(self):
        self.rect.x = 50
        self.rect.y = 90  
