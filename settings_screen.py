import pygame
from config import *

class ConfigScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.volume_music = 50
        self.volume_sound = 50
        self.selected_option = None
        self.selected_color = (255, 0, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = "music"
                elif event.key == pygame.K_DOWN:
                    self.selected_option = "sound"
                elif event.key == pygame.K_LEFT:
                    if self.selected_option == "music":
                        self.volume_music = max(0, self.volume_music - 10)
                    elif self.selected_option == "sound":
                        self.volume_sound = max(0, self.volume_sound - 10)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == "music":
                        self.volume_music = min(100, self.volume_music + 10)
                    elif self.selected_option == "sound":
                        self.volume_sound = min(100, self.volume_sound + 10)

    def display(self):
        self.screen.fill((0,0,0))
        text_music = self.font.render(f"Music Volume: {self.volume_music}", True, self.selected_color if self.selected_option == "music" else (white))
        text_sound = self.font.render(f"Sound Volume: {self.volume_sound}", True, self.selected_color if self.selected_option == "sound" else (white))
        text_exit = self.font.render("Press ESC to return", True, (white))

        self.screen.blit(text_music, (50, 50))
        self.screen.blit(text_sound, (50, 100))
        self.screen.blit(text_exit, (50, 150))

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Settings")

    config_screen = ConfigScreen(screen)
    running = True

    while running:
        config_screen.handle_events()
        config_screen.display()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()


