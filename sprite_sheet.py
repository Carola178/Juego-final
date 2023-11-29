import pygame
from config import *

class SpriteSheets:
    def __init__(self, image_sheet:pygame.surface, rows, cols, width, height, keys = None) -> None:
        
        self.image_sheet = image_sheet
        self.width = self.image_sheet.get_width()
        self.height = self.image_sheet.get_height()
        self.rows = rows
        self.cols = cols
        self.width_sprite = width
        self.height_sprite = height
        self.keys = keys

    
    def get_animation_dict(self, scale=1):
        
        self.width = scale * self.width
        self.height = scale * self.height
        self.width_sprite = scale * self.width_sprite
        self.height_sprite = scale * self.height_sprite        
        
        self.image_sheet = pygame.transform.scale(self.image_sheet, (self.width, self.height))
        
        contador_cols = 0

        animation_dict = {} 
        
        for row in range(self.rows): 
            animation_row = [] 
            
            for _ in range(self.cols): 
                animation_row.append(self.image_sheet.subsurface((contador_cols * self.width_sprite, row * self.height_sprite, self.width_sprite, self.height_sprite )))
                contador_cols +=1
                contador_cols = 0
            
            animation_dict [self.keys[row]] = animation_row 
        return animation_dict
    

#------------------------------------------------------------------------------------
    def get_animation_stars(self, scale=2):
        self.width_sprite *= scale
        self.height_sprite *= scale
        self.width *= scale
        self.height *= scale

        self.sheet_stars = pygame.transform.scale(self.image_sheet, (self.width, self.height))

        
        contador_cols = 0
        animation_stars = []
        for row in range(self.rows):
            for col in range(self.cols):
                frame = self.sheet_stars.subsurface((col * self.width_sprite, row * self.height_sprite, self.width_sprite, self.height_sprite))
                animation_stars.append(frame)

        return animation_stars

