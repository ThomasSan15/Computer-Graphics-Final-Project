# ==============================
#   UTILIDADES GENERALES
# ==============================

import pygame
import os

def openTopScoreFile():
    """Lee el archivo con el puntaje más alto registrado"""
    with open('TopScoreFile.txt') as file:
        topScore = int(file.read())
    file.close()
    return topScore


def saveTopScoreFile(topScore):
    """Guarda el nuevo record si SCORE es mayor al TOPSCORE anterior"""
    with open('TopScoreFile.txt', 'w') as file:
        file.write(str(topScore))
    file.close()


def gameImageLoad(imagefilepath, size):
    """Carga una imagen y la escala al tamaño especificado"""
    image = pygame.image.load(imagefilepath)
    image = pygame.transform.scale(image, (size[0], size[1]))
    return image


def textScreen(message, size=32, color=(255, 255, 255), shadow=True):
    """Renderiza texto con opción de sombra"""
    font = pygame.font.SysFont("consolas", size, bold=True)
    text = font.render(message, True, color)

    if shadow:
        shadow_surf = font.render(message, True, (0, 0, 0))
        return shadow_surf, text
    return None, text
