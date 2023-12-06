import pygame
from config import *
from sprite_sheet import SpriteSheets
from pygame.locals import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.game_title = "The jungle" 
        self.menu_items = ["Start", "Quit"]
        self.selected = 0
        self.background_image = pygame.image.load("./src/assets/images/background2.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT)) 



    def draw_menu(self):
        title_font = pygame.font.Font(None, 90)  
        title_text = title_font.render(self.game_title, True, black)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))  
        self.screen.blit(title_text, title_rect)
        
        menu_y = 250
        for idx, item in enumerate(self.menu_items):
            color = black
            if idx == self.selected:
                color = red
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, menu_y))
            self.screen.blit(text, text_rect)
            menu_y += 70

    def handle_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # Start the game
                    self.selected = 0 
                    return "start"
                elif self.selected == 1:
                    return "quit"
        return None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                action = self.handle_key_event(event)
                if action == "start":
                    return "start"
                elif action == "quit":
                    return "quit"

            self.screen.blit(self.background_image, (0, 0))
            self.draw_menu()
            pygame.display.flip()
