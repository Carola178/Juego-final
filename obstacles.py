import pygame
from config import *
from random import *

class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))

obstacle_images = [
        pygame.image.load("./src/assets/images/obstacle1.png"),
        pygame.image.load("./src/assets/images/obstacle2.png"),
        pygame.image.load("./src/assets/images/obstacle3.png"),
        pygame.image.load("./src/assets/images/obstacle4.png"),
    ]

obstacle_positions = []
for _ in range(4):
        pos_x = randint(0, WIDTH - WIDTH_OBSTACLE)
        pos_y = randint(0, HEIGHT - HEIGHT_OBSTACLE)
        obstacle_positions.append((pos_x, pos_y))

obstacles_group = pygame.sprite.Group()

for idx, image in enumerate(obstacle_images):
        x, y = obstacle_positions[idx]
        obstacle_instance = Obstacle(x, y, image)
        obstacles_group.add(obstacle_instance)
