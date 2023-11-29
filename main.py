import pygame
from config import *
from pygame.locals import *
from player import Player
from enemy import Enemy
from sprite_sheet import SpriteSheets
from plataforma import *
from sys import *
from random import *
from stars_enemy import Stars
from obstacles import Obstacle
from settings_screen import *
from coins import Coin


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size_screen)
        pygame.display.set_caption("Wizart's world")
        pygame.display.set_icon(pygame.image.load("./src/assets/images/icon.png"))
        self.all_sprites = pygame.sprite.Group()
        self.background = pygame.transform.scale(pygame.image.load("./src/assets/images/background.jpg"), (WIDTH, HEIGHT))
        self.music = pygame.mixer.music.load("./src/assets/sounds/musica_de_fondo.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.music_paused = False
        self.config_screen = ConfigScreen(self.screen)
        self.elapsed_time = 0  
        self.total_time = 30  
        self.player_vidas = 3
        self.score = 0
        self.current_screen = "game"
        
        
        
        #sonidos de fondo
        self.coin = pygame.mixer.Sound("./src/assets/sounds/sonido_moneda.mp3")
        self.victory = pygame.mixer.Sound("./src/assets/sounds/sonido_victoria.mp3")
        self.game_over_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_game_over.mp3")  
        
        #pausa (sonidos y fuente texto)
        self.pause_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_moneda.mp3")
        self.font = pygame.font.Font(None, 50)
        self.pause_text = self.font.render("Pause", True, (red))
        


        sprite_sheet_player = SpriteSheets(pygame.image.load("./src/assets/images/player.png").convert_alpha(), 5, 4, WIDTH_PLAYER, HEIGHT_PLAYER, ["idle", "right", "left", "front", "back"])

        
        self.coins_group = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        sprite_sheet_enemy = SpriteSheets(pygame.image.load("./src/assets/images/enemy.png").convert_alpha(), 4, 3, WIDTH_ENEMY, HEIGHT_ENEMY, ["back", "right", "front", "left",] )
        

        #enemy stars
        self.enemy_shooting = False 
        self.shoot_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_laser.mp3")
        
        #coins
        coin1 = Coin(450, 60, "./src/assets/images/coins.png")
        coin2 = Coin(190, 60, "./src/assets/images/coins.png")
        coin3 = Coin(870, 50, "./src/assets/images/coins.png")
        coin4 = Coin(120, 500, "./src/assets/images/coins.png")
        coin5 = Coin(850, 400, "./src/assets/images/coins.png")
        coin6 = Coin(550, 200, "./src/assets/images/coins.png")
        coin7 = Coin(850, 400, "./src/assets/images/coins.png")
        coin8 = Coin(360, 400, "./src/assets/images/coins.png")
        

        
        self.coins_group.add(coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8)


        
        self.elementos = [
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles1.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles2.png"), (WIDTH_OBSTACLE,HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles3.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles4.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles5.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacles4.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),                                    
        ]
        
        # Posiciones aleatorias para las imagenes
        self.positions = []
        for _ in range(len(self.elementos)):
            pos_x = randint(0, WIDTH - self.elementos[0].get_width())
            pos_y = randint(0, HEIGHT - self.elementos[0].get_height())
            self.positions.append((pos_x, pos_y))


        
        self.platforms = pygame.sprite.Group()
        Platform([self.all_sprites, self.platforms],(820, 480, 200, 80))
        Platform([self.all_sprites, self.platforms], (430, 315, 200, 80))
        Platform([self.all_sprites, self.platforms], (100, 100, 200, 80))
        Platform([self.all_sprites, self.platforms], (850, 100, 200, 80))
        Platform([self.all_sprites, self.platforms], (120, 500, 200, 80))
        
        self.obstacles_group = pygame.sprite.Group()
        
        self.player = Player([self.all_sprites], sprite_sheet_player)
        self.player.set_obstacles_group(self.obstacles_group)

        self.enemy = Enemy([self.all_sprites, self.enemies], sprite_sheet_enemy)
        self.paused = False
        

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                self.coins_group.update(self.coins_group)
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player.jump()
                    self.config_screen.handle_events()
                    if event.key == pygame.K_SPACE:
                        if self.current_screen == "game":
                            self.current_screen = "config"
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                            self.music_paused = True
                            self.pause_sound.play()
                        else:
                            self.current_screen = "game"
                            pygame.mixer.music.unpause()
                            self.music_paused = False
                    if event.key == K_e:
                        if self.enemy.alive():
                            Stars([self.all_sprites], self.enemy.rect.center, self.shoot_sound)
                            new_star = Stars([self.all_sprites], self.enemy.rect.midtop, self.shoot_sound)
                            self.all_sprites.add(new_star)
                            self.enemy_shooting = True

                if event.type == KEYUP:
                    if event.key == K_e:
                        self.enemy_shooting = False

            if self.current_screen == "game" and not self.paused:
                self.update()
                self.elapsed_time += self.clock.get_time() / 500
                if self.elapsed_time >= self.total_time:  
                    self.game_over() 

            self.draw() 
            if self.paused:
                text_rect = self.pause_text.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(self.pause_text, text_rect)
                self.config_screen.display()
                
    def update(self):
        #colisiones
        plataforma = pygame.sprite.spritecollide(self.player, self.platforms, False)
        
        for plataf in plataforma:
            if self.player.rect.bottom >= plataf.rect.top and self.player.speed_vert > 0:
                self.player.rect.bottom = plataf.rect.top
                self.player.speed_vert = 0
                

        coins_collected = pygame.sprite.spritecollide(self.player, self.coins_group, True)
        for coin in coins_collected:
            self.score += 10  

        # colisión con los obstáculos
        obstacles_hit = pygame.sprite.spritecollide(self.player, self.obstacles_group, True)
        for obstacle in obstacles_hit:
            self.score -= 20
            
        enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_collisions:
            self.player_vidas -= 1
            if self.player_vidas <= 0:
                self.game_over()
            else:
                self.player.reset_position()
                
        if self.music_paused:
            pygame.mixer.music.stop()
            

            
        self.all_sprites.update()
            
            
            
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.coins_group.draw(self.screen)
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            text_rect = self.pause_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(self.pause_text, text_rect)
        for idx, elemento in enumerate(self.elementos):
            pos_x, pos_y = self.positions[idx]
            self.screen.blit(elemento, (pos_x, pos_y))
            
        lives_text = self.font.render(f"Lives: {self.player_vidas}", True, grey, black)
        self.screen.blit(lives_text, (10, 10))
        
        timer_text = self.font.render(f"Time: {int(self.total_time - self.elapsed_time)}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH - 150, 10))
        
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (WIDTH - 150, 50))
        
        
        pygame.display.flip()

    def close(self):
        quit()
        sys.exit()

    def game_over(self):
        pygame.mixer.music.stop()  
        self.game_over_sound.play() 
        game_over_font = pygame.font.Font(None, 80)
        game_over_text = game_over_font.render("Game Over", True, red)
        text_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  
        self.close()

if __name__ == "__main__":
    game = Game()
    game.run()
