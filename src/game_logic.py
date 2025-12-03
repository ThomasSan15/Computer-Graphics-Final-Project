# ==============================
#   LÓGICA DEL JUEGO
# ==============================

import random
from pygame import Vector2
from src import config


def generate_random_location(player_pos):
    """Genera una posición aleatoria en pantalla alejada del jugador"""
    validLocation = False
    while not validLocation:
        asteroidPosX = random.randrange(0, config.SCREENWIDTH)
        asteroidPosY = random.randrange(0, config.SCREENHEIGHT)
        asteroidLocation = Vector2(asteroidPosX, asteroidPosY)
        if asteroidLocation.distance_to(player_pos) >= 100:  # Evita nacer encima del jugador
            validLocation = True
    return asteroidLocation


def check_asteroidCount_increase_stage(asteroidObjects):
    """Si ya no quedan asteroides, incrementa la etapa y genera más"""
    if len(asteroidObjects) == 0 and not config.GAMEOVER:
        config.STAGE += 1
        return True
    return False


def generate_asteroids(asteroidObjects, Asteroid, asteroidImgs):
    """Genera asteroides grandes dependiendo de la etapa actual"""
    for _ in range(config.STAGE):
        random_location = generate_random_location(Vector2(config.SCREENWIDTH // 2, config.SCREENHEIGHT // 2))
        asteroid_img_set = random.choice([asteroidImgs['asteroidImgA'], asteroidImgs['asteroidImgB'], 
                                          asteroidImgs['asteroidImgC'], asteroidImgs['asteroidImgD'],
                                          asteroidImgs['asteroidImgE'], asteroidImgs['asteroidImgF'],
                                          asteroidImgs['asteroidImgG']])
        asteroidObjects.append(Asteroid('large', random_location, asteroid_img_set, 
                                       asteroid_img_set['large'][0], asteroidImgs))


def resetAfterLosingALife(player, asteroidObjects, playerBullets):
    """Reinicia posición del jugador y asteroides tras perder vida"""
    import pygame
    
    player.pos = Vector2(config.SCREENWIDTH // 2, config.SCREENHEIGHT // 2)
    player.direction = Vector2(0, -1)
    player.velocity = Vector2()
    playerBullets.clear()

    if not config.GAMEOVER:
        for index, asteroidObject in enumerate(asteroidObjects):
            player_pos = Vector2(player.pos[0], player.pos[1])
            asteroidObject.pos = generate_random_location(player_pos)
        # Establecer el estado de impacto en lugar de bloquear con wait()
        config.HIT_BY_ASTEROID = True
        config.HIT_TIMER = 180  # 3 segundos a 60 FPS
    else:
        asteroidObjects.clear()


def calculateTotalNumAsteroids(asteroidObjects):
    """Devuelve la cantidad de asteroides restantes (incluyendo divisiones futuras)"""
    numAsteroids = 0
    for asteroidObject in asteroidObjects:
        if asteroidObject.size == 'large':
            numAsteroids += 7
        elif asteroidObject.size == 'medium':
            numAsteroids += 3
        else:
            numAsteroids += 1
    return numAsteroids
