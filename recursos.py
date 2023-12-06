import pygame
pygame.mixer.init()

class GestorRecursos:
    def __init__(self):
        self.imagenes = {}
        self.sonidos = {}

    def cargar_imagen(self, clave, ruta):
        imagen = pygame.image.load(ruta)
        self.imagenes[clave] = imagen
        return imagen

    def obtener_imagen(self, clave):
        return self.imagenes.get(clave)

    def cargar_sonido(self, clave, ruta):
        sonido = pygame.mixer.Sound(ruta)
        self.sonidos[clave] = sonido
        return sonido

    def obtener_sonido(self, clave):
        return self.sonidos.get(clave)

    def cargar_imagenes_escaladas(self, claves, rutas, escala):
        imagenes_escaladas = []
        for clave, ruta in zip(claves, rutas):
            imagen = pygame.transform.scale(pygame.image.load(ruta), escala)
            self.imagenes[clave] = imagen
            imagenes_escaladas.append(imagen)
        return imagenes_escaladas
# Uso del gestor de recursos
gestor = GestorRecursos()

# Cargar imágenes y sonidos
gestor.cargar_imagen('player', './src/assets/images/player.png')
gestor.cargar_imagen('enemy', './src/assets/images/enemy.png')
gestor.cargar_imagen('icono', './src/assets/images/icon.png')
gestor.cargar_imagen('coins', './src/assets/images/coins.png')
gestor.cargar_imagen('diamantes', './src/assets/images/diamantes.jpg')
gestor.cargar_imagen('background', './src/assets/images/background.jpg')
gestor.cargar_imagen('background2', './src/assets/images/background2.jpg')
gestor.cargar_imagen('fire-dragon', './src/assets/images/fire-dragon.png')
gestor.cargar_imagen('marco_final_score', './src/assets/images/marco_final_score.png')
gestor.cargar_imagen('obstacle1', './src/assets/images/obstacle1.png')
gestor.cargar_imagen('obstacle2', './src/assets/images/obstacle2.png')
gestor.cargar_imagen('obstacle3', './src/assets/images/obstacle3.png')
gestor.cargar_imagen('obstacle4', './src/assets/images/obstacle4.png')
gestor.cargar_imagen('obstacle5', './src/assets/images/obstacle5.png')
gestor.cargar_imagen('obstacle6', './src/assets/images/obstacle6.png')

#--------------------------------------------------------------------------

gestor.cargar_sonido('game_over', './src/assets/sounds/sonido_game_over.mp3')
gestor.cargar_sonido('victoria', './src/assets/sounds/sonido_victoria.mp3')
gestor.cargar_sonido('coin', './src/assets/sounds/sonido_moneda.mp3')
gestor.cargar_sonido('musica_fondo_inicio', './src/assets/sounds/musica_fondo_inicio.mp3')
gestor.cargar_sonido('musica_de_fondo', './src/assets/sounds/musica_de_fondo.mp3')
gestor.cargar_sonido('pausa', './src/assets/sounds/sonido_pausa.mp3')
gestor.cargar_sonido('laser', './src/assets/sounds/sonido_laser.mp3')

