# ==============================
#         BALAS
# ==============================

import pygame
from pygame import Vector2
from src import config


class Bullet:
    """Objeto proyectil disparado por el jugador"""

    def __init__(self, coOrds, direction):
        self.width = 4
        self.height = 4
        self.pos = Vector2(coOrds[0], coOrds[1])
        self.direction = Vector2(direction[0], direction[1])
        self.velocity = Vector2()
        self.speed = 8

    def move(self):
        """Movimiento recto constante"""
        self.pos += (self.direction * self.speed)

    def _check_if_offscreen(self):
        """Destruye bala si sale de pantalla"""
        if self.pos[0] < 0 or self.pos[0] > config.SCREENWIDTH or self.pos[1] < 0 or self.pos[1] > config.SCREENHEIGHT:
            return True

    def draw(self, window):
        """Dibuja bala y actualiza hitbox"""
        pygame.draw.rect(window, (255, 255, 255), [self.pos[0], self.pos[1], self.width, self.height])
        self.bulletRect = pygame.rect.Rect(int(self.pos[0]), int(self.pos[1]), self.width, self.height)
