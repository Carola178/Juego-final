# # import pygame
# # from config import *

# # class PlayerNameScreen:
# #     def __init__(self, screen):
# #         self.screen = screen
# #         self.text = ''
# #         self.font = pygame.font.Font(None, 32)
# #         self.input_box = pygame.Rect(100, 100, 140, 32)
# #         self.input_box.center = screen.get_rect().center
# #         self.active = False
# #         self.done = False
# #         self.title_font = pygame.font.Font(None, 36)
# #         self.title_text = self.title_font.render("Ingrese el nombre de su jugador:", True, (black))
# #         self.input_width = 200
# #         self.is_done = False
        
# #         self.ok_button_width = self.input_box.width // 2  
# #         self.ok_button = pygame.Rect(
# #             (self.screen.get_width() - self.ok_button_width) // 2, 
# #             self.input_box.y + self.input_box.height + 20, self.ok_button_width, 30)
# #         self.button_color = pygame.Color('dodgerblue2')
# #         self.button_text = pygame.font.Font(None, 24).render('OK', True, white)


# #         self.background_image = pygame.image.load("./src/assets/images/background2.jpg").convert()
# #         self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
# #         self.jugar_button = pygame.image.load("./src/assets/images/flecha_inicio.jpg")
# #         self.jugar_button = pygame.transform.scale(self.jugar_button, (80, 80))         
# #         self.jugar_button_rect = self.jugar_button.get_rect()
# #         self.jugar_button_rect.bottomright = (self.screen.get_width() - 30, self.screen.get_height() - 30)  # Posición de la imagen

# #         self.jugar_text = pygame.font.Font(None, 32).render('Jugar', True, black)
# #         self.jugar_text_rect = self.jugar_text.get_rect()
# #         self.jugar_text_rect.midright = (self.jugar_button_rect.midright[0], self.jugar_button_rect.bottom + 8) 

# #     def draw(self):
# #         self.screen.blit(self.background_image, (0, 0))
# #         title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
# #         self.screen.blit(self.title_text, title_rect)


# #         txt_surface = self.font.render(self.text, True, black)
# #         width = max(200, txt_surface.get_width() + 10)
# #         self.input_box.w = width

# #         pygame.draw.rect(self.screen, black, self.input_box, 2)
# #         self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

# #         pygame.draw.rect(self.screen, self.button_color, self.ok_button)
# #         self.screen.blit(self.button_text, (self.ok_button.x + 10, self.ok_button.y + 8))
        
# #         self.screen.blit(self.jugar_button, self.jugar_button_rect)
# #         self.screen.blit(self.jugar_text, self.jugar_text_rect)
        

# #     def handle_event(self, event):
# #         if event.type == pygame.MOUSEBUTTONDOWN:
            
# #             if self.input_box.collidepoint(event.pos):
# #                 self.active = True
# #             else:
# #                 self.active = False
            
# #             if self.ok_button.collidepoint(event.pos):
# #                 print(self.text)
# #                 self.text = ''

# #         if event.type == pygame.KEYDOWN:
# #             if self.active:
# #                 if event.key == pygame.K_RETURN:
# #                     self.done = True 
# #                 elif event.key == pygame.K_BACKSPACE:
# #                     self.text = self.text[:-1]
# #                 else:
# #                     self.text += event.unicode

# #     def update(self):
# #         if self.done and self.text != "":
# #             self.done = False  
# #             self.player_name = self.text 

# #     def get_player_name(self):
# #         return self.player_name
        
# #     def get_text(self):
# #         return self.text
# #-------------------------------------------------------------------------------------------------
# import pygame
# from config import *
# from sprite_sheet import SpriteSheets
# from pygame.locals import *


# class Menu:
#     def __init__(self, screen):
#         self.screen = screen
#         self.font = pygame.font.Font(None, 50)
#         self.game_title = "The jungle" 
#         self.menu_items = ["Comenzar",  "Salir"]
#         self.selected = 0
#         self.background_image = pygame.image.load("./src/assets/images/background2.jpg").convert()
#         self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT)) 



#     def draw_menu(self):
#         title_font = pygame.font.Font(None, 90)  
#         title_text = title_font.render(self.game_title, True, black)
#         title_rect = title_text.get_rect(center=(WIDTH // 2, 100))  
#         self.screen.blit(title_text, title_rect)
        
#         menu_y = 250
#         for idx, item in enumerate(self.menu_items):
#             color = black
#             if idx == self.selected:
#                 color = red
#             text = self.font.render(item, True, color)
#             text_rect = text.get_rect(center=(WIDTH // 2, menu_y))
#             self.screen.blit(text, text_rect)
#             menu_y += 70

#     def handle_key_event(self, event):
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 self.selected = (self.selected - 1) % len(self.menu_items)
#             elif event.key == pygame.K_DOWN:
#                 self.selected = (self.selected + 1) % len(self.menu_items)
#             elif event.key == pygame.K_RETURN:
#                 if self.selected == 0:
#                     # Start the game
#                     self.selected = 0 
#                     return "Comenzar"
#                 elif self.selected == 1:
#                     return "Salir"
#         return None

#     def run(self):
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     return "Salir"
#                 action = self.handle_key_event(event)
#                 if action == "Comenzar":
#                     return "Comenzar"
#                 elif action == "Salir":
#                     return "Salir"

#             self.screen.blit(self.background_image, (0, 0))
#             self.draw_menu()
#             pygame.display.flip()
