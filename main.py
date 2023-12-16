import pygame
from config import *
from pygame.locals import *
from player import Player
from enemy import Enemy
from sprite_sheet import SpriteSheets
from plataforma import *
from sys import *
from random import *
from obstacles import Obstacle
from settings_screen import *
from coins import Coin
from pantalla_inicio import Menu
from diamantes import Diamante
from nivel2 import Nivel2
from nivel3 import Nivel3
from base_de_datos import DataBase

class Nivel:
    def __init__(self, level_number):
        self.level_number = level_number


class Nivel1(Nivel):
    def __init__(self, level_number=1):
        super().__init__(level_number)  
        pygame.init()
        self.in_menu = True
        self.in_game = False
        self.db = DataBase()

    def init(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size_screen)
        pygame.display.set_caption("The jungle")
        pygame.display.set_icon(pygame.image.load("./src/assets/images/icon.png"))
        self.background = pygame.transform.scale(pygame.image.load("./src/assets/images/background.jpg"), (WIDTH, HEIGHT))    
        
        
        self.music_paused = False
        self.elapsed_time = 0  
        self.total_time = 45 
        self.player_vidas = 3
        self.score = 0
        self.current_screen = "game"
        
        #pantalla de inicio
        # Obtener la fecha y hora actual
        self.menu = Menu(self.screen)
        self.countdown_active = True
        self.countdown_duration = 3
        self.countdown_elapsed = 0
        
        self.option_color1 = black
        self.option_hover_color1 = red  
        self.option_color2 = black
        self.option_hover_color2 = red 
        self.option_font = pygame.font.Font(None, 36)
        
        #sonidos de fondo
        self.coin_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_moneda.mp3")
        self.victory_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_victoria.mp3")
        self.game_over_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_game_over.mp3")
        self.diamantes_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_diamantes.mp3")
        
        #pausa (sonidos y fuente texto)
        self.pause_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_pausa.mp3")
        self.font = pygame.font.Font(None, 50)
        self.pause_text = self.font.render("Pause", True, (red))
        
        self.menu_background = pygame.image.load("./src/assets/images/background2.jpg")
        self.musica_fondo_inicio = pygame.mixer.music.load("./src/assets/sounds/musica_fondo_inicio.mp3")
        self.final_score_image = pygame.image.load("./src/assets/images/marco_final_score.png").convert_alpha()
        
        #enemy stars
        self.enemies = []
        self.enemy_shooting = False 
        self.shoot_sound = pygame.mixer.Sound("./src/assets/sounds/sonido_laser.mp3")
        self.obstacles_touched = set()


        # Creación de instancias de SpriteSheets
        sprite_sheet_player = SpriteSheets(pygame.image.load("./src/assets/images/player.png").convert_alpha(), 5, 4, WIDTH_PLAYER, HEIGHT_PLAYER, ["idle", "right", "left", "front", "back"])
        sprite_sheet_enemy = SpriteSheets(pygame.image.load("./src/assets/images/enemy.png").convert_alpha(), 4, 3, WIDTH_ENEMY, HEIGHT_ENEMY, ["left", "right", "front", "back"])
        

        # Creación de grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.invisible_platforms_group = pygame.sprite.Group()
        self.diamantes_group = pygame.sprite.Group()
        
        # Creación del jugador y enemigo
        self.player = Player([self.all_sprites], sprite_sheet_player)
        self.player.set_obstacles_group(self.obstacles_group)
        
        
        enemies_positions = [(WIDTH - 50, 0), (WIDTH - 100, 0)]  
        for pos in enemies_positions:
            enemy = Enemy([self.all_sprites, self.enemy_group], sprite_sheet_enemy)
            enemy.rect.topleft = pos
            self.enemies.append(enemy) 

        # Asignar al jugador a cada enemigo
        for enemy in self.enemies:
            enemy.set_player(self.player)
        
        self.paused = False



        self.elementos = [
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle1.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle2.png"), (WIDTH_OBSTACLE,HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle3.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle4.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle5.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),
            pygame.transform.scale(pygame.image.load("./src/assets/images/obstacle6.png"), (WIDTH_OBSTACLE, HEIGHT_OBSTACLE)),                                    
        ]
        
        # Posiciones aleatorias para las imagenes
        self.positions = []
        for _ in range(len(self.elementos)):
            pos_x = randint(0, WIDTH - self.elementos[0].get_width())
            pos_y = randint(0, HEIGHT - self.elementos[0].get_height())
            self.positions.append((pos_x, pos_y))

        for idx, elemento in enumerate(self.elementos):
            pos_x, pos_y = self.positions[idx]
            obstacle = Obstacle(pos_x, pos_y, elemento)
            self.obstacles_group.add(obstacle)
            
        for coin in range(30):
            pos_x = randint(0, WIDTH - WIDTH_COINS)
            pos_y = randint(0, HEIGHT - HEIGHT_COINS)
            coin = Coin(pos_x, pos_y, "./src/assets/images/coins.png")
            self.coins_group.add(coin)
            
        for diamante in range(15):
            pos_x = randint(0, WIDTH - WIDTH_COINS)
            pos_y = randint(0, HEIGHT - HEIGHT_COINS)
            diamante = Diamante(pos_x, pos_y, "./src/assets/images/diamantes.jpg")
            self.diamantes_group.add(diamante)            

    # plataforma invisible
        self.platform1 = InvisiblePlatform(100, 315, 40, 50)
        self.platform2 = InvisiblePlatform(330, 200, 40, 50)
        self.platform3 = InvisiblePlatform(750, 200, 40, 50)
        self.platform4 = InvisiblePlatform(1010, 315, 40, 50)

        self.invisible_platforms_group.add(self.platform1, self.platform2, self.platform3, self.platform4)

    def start_timer(self):
        self.timer_active = True
        self.timer_elapsed = 0
    
        #icono de menu de opciones

        self.initial_state()  

    def initial_state(self):
        self.elapsed_time = 0
        self.score = 0
        self.player_vidas = 3

        self.player.reset_position()  
        self.coins_group.empty()
        
    def run(self, screen):
            self.screen = screen
            running = True
            player_name_screen = None
            result = None
            countdown_start = pygame.time.get_ticks()
            self.init()
            in_menu = True
            in_name_screen = False

            while running:
                self.clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            self.player.jump()
                        elif event.key == pygame.K_SPACE:
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

                if in_menu and not in_name_screen:
                    pygame.mixer.music.play(-1)
                    self.screen.blit(self.menu_background, (0, 0))
                    action = self.menu.run()

                    if action == "Comenzar":
                        self.countdown_active = True
                        in_menu = False
                        pygame.mixer.music.stop()
                        self.musica_fondo = pygame.mixer.music.load("./src/assets/sounds/musica_de_fondo.mp3")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.2)

                    elif action == "Salir":
                        running = False

                if self.countdown_active:
                    self.screen.fill(black)
                    current_time = pygame.time.get_ticks()
                    countdown_elapsed = (current_time - countdown_start) / 1000 
                    countdown_number = 3 - int(countdown_elapsed)

                    if countdown_number > 0:
                        countdown_text = self.font.render(str(countdown_number), True, white)
                    else:
                        countdown_text = self.font.render("GO!", True, white)
                    text_rect = countdown_text.get_rect(center=self.screen.get_rect().center)
                    self.screen.blit(countdown_text, text_rect)

                    if countdown_number >= 1 and countdown_number <= 3:
                        pygame.mixer.music.pause()

                    pygame.display.flip()

                    if countdown_number <= 0:
                        pygame.mixer.music.unpause()
                        self.countdown_active = False
                        self.in_game = True
                        self.elapsed_time = 0

                if self.in_game and not self.paused:
                    self.update()
                    self.draw()
                    self.elapsed_time += self.clock.get_time() / 1000

                    if self.elapsed_time >= self.total_time:
                        self.game_over()

                if self.paused and self.current_screen == "game":
                    text_rect = self.pause_text.get_rect(center=self.screen.get_rect().center)
                    self.screen.blit(self.pause_text, text_rect)

                if player_name_screen:
                    player_name_screen.handle_event(event)
                    result = player_name_screen.update()
                    

            
                    if result == "Menu":
                        in_menu = True  
                        in_name_screen = False
                        player_name_screen = None
                    elif result == "Done":
                        self.player_name = player_name_screen.text
                        in_menu = True
                        in_name_screen = False
                        player_name_screen = None

                pygame.display.flip()

            pygame.quit()
    
    def reset_level(self):  # Nuevo método para reiniciar el nivel
        # Lógica para restablecer las variables y el estado del nivel
        self.in_game = True
        self.score = 0        
    
    
    def show_score_screen(self):
        pygame.mixer.music.stop()
        final_score = self.score
        option_color1 = black
        option_hover_color1 = red  
        option_color2 = black
        option_hover_color2 = red  


        original_image = pygame.image.load("./src/assets/images/marco_final_score.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (1000, 649))
        image_width, image_height = scaled_image.get_size()

        self.screen = pygame.display.set_mode((image_width, image_height))

        self.screen.fill(white)

        coordenada_x = (self.screen.get_width() - image_width) // 2
        coordenada_y = (self.screen.get_height() - image_height) // 2

        self.screen.blit(scaled_image, (coordenada_x, coordenada_y))

        score_font = pygame.font.Font(None, 60)
        score_text = score_font.render(f"Final Score: {final_score}", True, (black))
        
        # Calcula la posición para centrar el texto en la parte superior
        text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(score_text, text_rect)
        
        with open('puntuaciones.txt', 'a') as file:
            file.write(f"Puntuacion: {self.score}\n")

        self.save_score_to_database()
        
        # Menú de opciones
        option_font = pygame.font.Font(None, 36)
        option_text1 = option_font.render("Continuar", True, (black))
        option_text2 = option_font.render("Salir", True, (black))

        option_rect1 = option_text1.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        option_rect2 = option_text2.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))

        self.screen.blit(option_text1, option_rect1)
        self.screen.blit(option_text2, option_rect2)

        pygame.display.flip()

        pygame.mixer.music.stop()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if option_rect1.collidepoint(mouse_pos):
                        self.next_level_menu()  

                    elif option_rect2.collidepoint(mouse_pos):
                        self.close()
                        
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if option_rect1.collidepoint(mouse_pos):
                        option_color1 = option_hover_color1  
                        option_color2 = black  
                    else:
                        option_color1 = black

                    if option_rect2.collidepoint(mouse_pos):
                        option_color2 = option_hover_color2 
                        option_color1 = black  
                    else:
                        option_color2 = black

            # Blit de textos con colores actualizados
            option_text1 = option_font.render("Continuar", True, option_color1)
            option_text2 = option_font.render("Salir", True, option_color2)

            self.screen.blit(option_text1, option_rect1)
            self.screen.blit(option_text2, option_rect2)

            pygame.display.flip()

    def save_score_to_database(self):
        player_id = 1  # Supongamos que hay un solo jugador por ahora
        game_id = self.level_number  # Usamos el número de nivel como game_id
        score = self.score  # El puntaje actual del jugador
        
        # Llama al método de tu objeto de base de datos para agregar el puntaje
        self.db.add_score(player_id, game_id, score)
        
    def next_level_menu(self):
        self.screen.fill(black)
        next_level_font = pygame.font.Font(None, 50)
        next_level_text = next_level_font.render("Seleccionar siguiente nivel:", True, (white))
        text_rect = next_level_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(next_level_text, text_rect)

        option_font = pygame.font.Font(None, 36)
        texto_nivel2 = option_font.render("Nivel 2", True, (white))
        texto_nivel3 = option_font.render("Nivel 3", True, (white))

        nivel2 = texto_nivel2.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        nivel3 = texto_nivel3.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))

        self.screen.blit(texto_nivel2, nivel2)
        self.screen.blit(texto_nivel3, nivel3)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if nivel2.collidepoint(mouse_pos):
                        self.start_level(Nivel2(level_number=2))
                        self.show_countdown("Nivel 2")
                        running = False  
                    elif nivel3.collidepoint(mouse_pos):
                        self.start_level(Nivel3(level_number=3))
                        self.show_countdown("Nivel 3")
                        running = False  
            mouse_pos = pygame.mouse.get_pos()
            if nivel2.collidepoint(mouse_pos):
                texto_nivel2 = option_font.render("Nivel 2", True, (red))
            else:
                texto_nivel2 = option_font.render("Nivel 2", True, (white))

            if nivel3.collidepoint(mouse_pos):
                texto_nivel3 = option_font.render("Nivel 3", True, (red))
            else:
                texto_nivel3 = option_font.render("Nivel 3", True, (white))

                # Resto del código para blit de textos con colores actualizados
            self.screen.blit(texto_nivel2, nivel2)
            self.screen.blit(texto_nivel3, nivel3)
                
            pygame.display.flip()
            

    def show_countdown(self):
        countdown_start = pygame.time.get_ticks()
        countdown_duration = 3  # Duración de la cuenta regresiva en segundos

        while True:
            current_time = pygame.time.get_ticks()
            countdown_elapsed = (current_time - countdown_start) / 1000
            countdown_number = countdown_duration - int(countdown_elapsed)

            if countdown_number > 0:
                countdown_text = self.font.render(str(countdown_number), True, white)
            else:
                break  # Si la cuenta llega a cero, salir del bucle

            # Mostrar el texto de la cuenta regresiva en la pantalla
            text_rect = countdown_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(countdown_text, text_rect)
            pygame.display.flip()

        # Cambiar al siguiente nivel una vez que la cuenta regresiva termine
        if self.level_number == 1:
            self.start_level(Nivel2(level_number=2))
        elif self.level_number == 2:
            self.start_level(Nivel3(level_number=3))

    
    def start_level(self, level_instance):
        level_instance.run(self.screen)
        
        
        pygame.display.flip()
    
    
        
    def update(self):
        self.score += 1
        #colisiones player y plataformas
        if pygame.sprite.spritecollide(self.player, self.invisible_platforms_group, False):
            for plataf in self.invisible_platforms_group:
                if self.player.rect.bottom >= plataf.rect.top and self.player.speed_vert > 0:
                    self.player.rect.bottom = plataf.rect.top
                    self.player.speed_vert = 0
                    
        #colisiones con monedas
        coins_collected = pygame.sprite.spritecollide(self.player, self.coins_group, True)
        for coin in coins_collected:
            self.score += 1
            self.coin_sound.play()
            if len(self.coins_group) == 0:
                self.in_game = False
                self.victory_sound.play()
                self.show_score_screen()
        
        #colisiones con diamantes
        diamantes_collected = pygame.sprite.spritecollide(self.player, self.diamantes_group, True)
        for diamante in diamantes_collected:
            self.score += 3
            self.coin_sound.play()
            if len(self.diamantes_group) == 0:
                self.in_game = False
                self.diamantes_sound.play()
                self.show_score_screen()
                
        # colisión con los obstáculos
        obstacles_hit = pygame.sprite.spritecollide(self.player, self.obstacles_group, False)
        for obstacle in obstacles_hit:
            if obstacle not in self.obstacles_touched:  
                self.obstacles_touched.add(obstacle)  
                self.elapsed_time += 2  
                if self.elapsed_time >= self.total_time:
                    self.game_over() 
        
        #colision con enemigo    
        enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemy_group, False)
        for enemy in enemy_collisions:
                self.player.reset_position()
                
        if self.music_paused:
            pygame.mixer.music.stop()
            
        for enemy in self.enemies:
            enemy.update()
            
        self.all_sprites.update()
        
        if self.elapsed_time <= 0 and len(self.coins_group) == 0 and len(self.diamantes_group) == 0:
            # Si se agotó el tiempo y se recogieron todas las monedas y diamantes, mostrar pantalla final
            self.show_score_screen()
        elif self.elapsed_time >= self.total_time:
            self.save_score_to_database()
            self.show_score_screen()              
            
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.coins_group.draw(self.screen)
        self.diamantes_group.draw(self.screen)
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            text_rect = self.pause_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(self.pause_text, text_rect)
        for idx, elemento in enumerate(self.elementos):
            pos_x, pos_y = self.positions[idx]
            self.screen.blit(elemento, (pos_x, pos_y))
            
        lives_text = self.font.render(f"Lives: {self.player_vidas}", True, grey, black)
        self.screen.blit(lives_text, (10, 10))
        
        timer_text = self.font.render(f"Time: {int(self.total_time - self.elapsed_time)}", True, (black))
        self.screen.blit(timer_text, (WIDTH - 150, 10))
        
        score_text = self.font.render(f"Score: {self.score}", True, (black))
        self.screen.blit(score_text, (WIDTH - 150, 50))
        
        pygame.display.flip()

    def close(self):
        quit()


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
        
class Juego:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size_screen)
        pygame.display.set_caption("The jungle")
        self.rank_shown = False
        self.games_played = 0
        self.db = DataBase()

    def run(self):
        running = True
        current_level = 1
        nivel = None

        while running:
            if current_level == 1:
                nivel = Nivel1(level_number=current_level)
            elif current_level == 2:
                nivel = Nivel2(level_number=current_level)
            elif current_level == 3:
                nivel = Nivel3(level_number=current_level)

            nivel.run(self.screen)

            if nivel.current_screen == "game":
                self.games_played += 1
                self.save_score_to_database(nivel.score, current_level)
                current_level += 1

            if current_level > 3:
                running = False

    def save_score_to_database(self, score, level_number):
        player_id = 1  # Supongamos que hay un solo jugador por ahora
        game_id = level_number  # Esto podría ser el número de nivel o un identificador único del juego
        self.db.add_score(player_id, game_id, score)


if __name__ == "__main__":
    game = Juego()
    game.run()
    pygame.quit()