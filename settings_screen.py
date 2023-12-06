import pygame
from config import *
from pygame.locals import *


class Menu:
    def __init__(self, screen):
        self.screen = screen

    def show_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            self.screen.fill((white))  

            pygame.display.flip()

        pygame.quit()

