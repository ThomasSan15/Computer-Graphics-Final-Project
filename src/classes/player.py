# ==============================
#       CLASE PLAYER
# ==============================

import pygame
from pygame import Vector2
from src import config


class Player:
    """Jugador/Nave controlada por el usuario"""

    def __init__(self, coOrds, img):
        self.img = img
        self.imgRect = self.img.get_rect()
        self.x, self.y = coOrds
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.imgRect.x = self.x - self.width // 2
        self.imgRect.y = self.y - self.height // 2
        self.pos = Vector2(self.imgRect.x, self.imgRect.y)
        self.direction = Vector2(0, -1)
        self.velocity = Vector2()
        self.rotation_speed = config.OBJECT_ROTATION_SPEED
        self.speed = config.OBJECT_SPEED

    def accelerate(self):
        """Aumenta velocidad en la dirección apuntada"""
        self.velocity += self.direction * self.speed
        if self.velocity.length() > 4:  # Velocidad máxima
            self.velocity.scale_to_length(4)

    def rotation(self, rotation=1):
        """Rota la nave"""
        angle = self.rotation_speed * rotation
        self.direction.rotate_ip(angle)

    def _wrap_to_screen(self, position):
        """Hace que el jugador aparezca del otro lado de la pantalla"""
        self.x, self.y = position
        return Vector2(self.x % config.SCREENWIDTH, self.y % config.SCREENHEIGHT)

    def move(self):
        """Actualiza movimiento"""
        self.pos = self._wrap_to_screen(self.pos + self.velocity)
        self.imgRect.x, self.imgRect.y = self.pos[0] - self.width // 2, self.pos[1] - self.height // 2

    def draw(self, window):
        """Dibuja la nave rotando correctamente"""
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_img = pygame.transform.rotozoom(self.img, angle, 1.0)
        rotated_img_size = Vector2(rotated_img.get_size())
        blit_pos = self.pos - rotated_img_size * 0.5
        window.blit(rotated_img, blit_pos)
