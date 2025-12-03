# ==============================
#       ASTEROIDES
# ==============================

import pygame
from pygame import Vector2
import random
from src.classes.player import Player
from src import config


class Asteroid(Player):
    """Asteroide con rotación, colisión y división"""

    def __init__(self, size, coOrds=(0, 0), imgSet=None, img=None, asteroidImgs=None):
        # No llamar a super().__init__() para evitar problemas con la imagen
        self.size = size
        self.imgSet = imgSet
        self.asteroidImgs = asteroidImgs
        
        # Inicialización de Player
        self.img = img
        self.imgRect = self.img.get_rect()
        self.x, self.y = coOrds
        self.width = self.img.get_width() // 2
        self.height = self.img.get_height() // 2
        self.imgRect.x = self.x - self.width // 2
        self.imgRect.y = self.y - self.height // 2
        self.imgRect = pygame.rect.Rect(self.imgRect.x, self.imgRect.y, self.width, self.height)
        
        self.pos = Vector2(self.imgRect.x, self.imgRect.y)
        self.direction = Vector2(0, -1)
        self.velocity = Vector2()
        self.rotation_speed = config.OBJECT_ROTATION_SPEED
        self.speed = config.OBJECT_SPEED
        
        # Movimiento aleatorio
        self.direction = Vector2(random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100)
        self.speed = random.randrange(3, 6)

        # Animación
        self.imgInd = 0
        self.imgIndex = 0
        self.animate_speed = random.randrange(3, 7)

        # Vida y puntaje según tamaño
        self.health = 3 if self.size == 'large' else 2 if self.size == 'medium' else 1
        self.score = 10 if self.size == 'large' else 20 if self.size == 'medium' else 50

    def accelerate(self):
        """Actualiza velocidad base"""
        self.velocity = self.direction * self.speed

    def _animate_image(self):
        """Cambia sprite para animar rotación"""
        self.imgInd += 1
        if self.imgInd % self.animate_speed == 0:
            self.imgIndex = self.imgInd // self.animate_speed
        if self.imgIndex == len(self.imgSet[self.size]) - 1:
            self.imgInd = 0
            self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]

    def move(self):
        """Actualiza movimiento y aplica velocidad"""
        self.pos = Vector2(self.pos[0] % config.SCREENWIDTH, self.pos[1] % config.SCREENHEIGHT)
        self.pos += self.velocity
        self.imgRect.x, self.imgRect.y = self.pos[0] - self.width // 2, self.pos[1] - self.height // 2
        self.accelerate()
