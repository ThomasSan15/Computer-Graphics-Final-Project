# ==============================
#   CARGA DE ASSETS
# ==============================

import pygame
import os
from src.utils.general import gameImageLoad


def asteroidImageLoading(AsteroidImgA, AsteroidImgB, AsteroidImgC, 
                         AsteroidImgD, AsteroidImgE, AsteroidImgF, AsteroidImgG):
    """Carga en memoria todas las imágenes de asteroides según su tamaño"""
    large = 180
    medium = 125
    small = 75
    for imgSize in ['large', 'medium', 'small']:  # Recorre carpetas
        if imgSize == 'large':
            imgSpriteSize = large
        elif imgSize == 'medium':
            imgSpriteSize = medium
        else:
            imgSpriteSize = small
        
        # Carga imágenes dependiendo del prefijo del archivo
        for item in os.listdir(f'assets/asteroids/{imgSize}'):
            if str(item)[:2] == 'a1':
                AsteroidImgA[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'a3':
                AsteroidImgB[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b1':
                AsteroidImgC[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b3':
                AsteroidImgD[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c1':
                AsteroidImgE[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c3':
                AsteroidImgF[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c4':
                AsteroidImgG[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))


def loadAllAssets():
    """Carga todos los assets del juego"""
    from src import config
    
    bgImg = gameImageLoad('assets/mapa.png', (config.SCREENWIDTH, config.SCREENHEIGHT))
    
    # Diccionarios donde se guardarán sprites animados
    asteroidImgA = {'large': [], 'medium': [], 'small': []}
    asteroidImgB = {'large': [], 'medium': [], 'small': []}
    asteroidImgC = {'large': [], 'medium': [], 'small': []}
    asteroidImgD = {'large': [], 'medium': [], 'small': []}
    asteroidImgE = {'large': [], 'medium': [], 'small': []}
    asteroidImgF = {'large': [], 'medium': [], 'small': []}
    asteroidImgG = {'large': [], 'medium': [], 'small': []}
    
    playerImg = gameImageLoad('assets/Nave.png', (65, 65))
    
    # Cargador de sprites de asteroides
    asteroidImageLoading(asteroidImgA, asteroidImgB, asteroidImgC, 
                        asteroidImgD, asteroidImgE, asteroidImgF, asteroidImgG)
    
    # Corazón de vida
    heartImg = pygame.image.load("assets/corazon.png").convert_alpha()
    heartImg = pygame.transform.scale(heartImg, (32, 32))
    
    # Sonidos
    shootSound = pygame.mixer.Sound('assets/sounds/laser.wav')
    shootSound.set_volume(0.3)  # Reducir volumen del disparo
    explSound = pygame.mixer.Sound('assets/sounds/bangSmall.wav')
    shipExplSound = pygame.mixer.Sound('assets/sounds/bangLarge.wav')
    
    # Icono de ventana
    icnImg = gameImageLoad('assets/Nave.png', (20, 20))
    icnImg = pygame.transform.rotate(icnImg, -90)
    
    return {
        'bgImg': bgImg,
        'playerImg': playerImg,
        'heartImg': heartImg,
        'asteroidImgA': asteroidImgA,
        'asteroidImgB': asteroidImgB,
        'asteroidImgC': asteroidImgC,
        'asteroidImgD': asteroidImgD,
        'asteroidImgE': asteroidImgE,
        'asteroidImgF': asteroidImgF,
        'asteroidImgG': asteroidImgG,
        'shootSound': shootSound,
        'explSound': explSound,
        'shipExplSound': shipExplSound,
        'icnImg': icnImg
    }
