import sys
import os
import pygame
from pygame import Vector2

pygame.init()  # Inicializa pygame

# ==============================
#   IMPORTAR MÓDULOS
# ==============================

from src import config
from src.utils.general import openTopScoreFile, saveTopScoreFile
from src.assets_loader import loadAllAssets
from src.classes.player import Player
from src.classes.bullet import Bullet
from src.classes.asteroid import Asteroid
from src.game_logic import (
    generate_random_location,
    check_asteroidCount_increase_stage,
    generate_asteroids,
    resetAfterLosingALife,
    calculateTotalNumAsteroids
)
from src.rendering import gameWindowUpdating
from src.event_handler import handle_events, handle_player_controls

# ==============================
#   INICIALIZAR PANTALLA
# ==============================

config.GAMESCREEN = pygame.display.set_mode((config.SCREENWIDTH, config.SCREENHEIGHT))
pygame.display.set_caption('Asteroids')

# Cargar assets
assets = loadAllAssets()
pygame.display.set_icon(assets['icnImg'])

# ==============================
#   VARIABLES DEL JUEGO
# ==============================

config.TOPSCORE = openTopScoreFile()
config.STAGE = 1
config.LIVES = 3
config.GAMEOVER = False
config.SCORE = 0

player = Player((config.SCREENWIDTH // 2, config.SCREENHEIGHT // 2), assets['playerImg'])
playerBullets = []
asteroidObjects = []

generate_asteroids(asteroidObjects, Asteroid, assets)

# ==============================
#      BUCLE PRINCIPAL
# ==============================

RUNGAME = True
while RUNGAME:

    if not config.GAMEOVER:

        # Cambiar etapa si no quedan asteroides
        if check_asteroidCount_increase_stage(asteroidObjects):
            generate_asteroids(asteroidObjects, Asteroid, assets)

        # -------------------------
        # Movimiento de jugador
        # -------------------------
        player.move()

        # -------------------------
        # Movimiento de Balas
        # -------------------------
        for ind, bullet in enumerate(playerBullets):
            bullet.move()

            # Si sale de pantalla, se elimina
            if bullet._check_if_offscreen():
                del playerBullets[ind]
                break

        # -------------------------
        # Movimiento de Asteroides + Colisiones
        # -------------------------
        for ind, asteroidObject in enumerate(asteroidObjects):
            asteroidObject.move()

            # Colisión bala ↔ asteroide
            for index, bullet in enumerate(playerBullets):
                if bullet.bulletRect.colliderect(asteroidObject.imgRect):
                    asteroidObject.health -= 1
                    config.SCORE += asteroidObject.score

                    if asteroidObject.health == 0:
                        # Asteroide grande se divide
                        if asteroidObject.size == 'large':
                            new_pos = Vector2(asteroidObject.pos)
                            asteroidObjects.append(Asteroid('medium', new_pos, asteroidObject.imgSet, 
                                                           asteroidObject.imgSet['medium'][0], assets))
                            asteroidObjects.append(Asteroid('medium', new_pos, asteroidObject.imgSet,
                                                           asteroidObject.imgSet['medium'][0], assets))

                        # Mediano → pequeño
                        elif asteroidObject.size == 'medium':
                            new_pos = Vector2(asteroidObject.pos)
                            asteroidObjects.append(Asteroid('small', new_pos, asteroidObject.imgSet,
                                                           asteroidObject.imgSet['small'][0], assets))
                            asteroidObjects.append(Asteroid('small', new_pos, asteroidObject.imgSet,
                                                           asteroidObject.imgSet['small'][0], assets))

                        del asteroidObjects[ind]
                        assets['explSound'].play()

                    del playerBullets[index]
                    break

            # Colisión nave ↔ asteroide
            if asteroidObject.imgRect.colliderect(player.imgRect):
                config.LIVES -= 1
                assets['shipExplSound'].play()

                if config.LIVES <= 0:
                    config.GAMEOVER = True
                    saveTopScoreFile(config.SCORE)
                    config.SCORE = 0
                else:
                    resetAfterLosingALife(player, asteroidObjects, playerBullets)
                    if ind < len(asteroidObjects):
                        del asteroidObjects[ind]
                    break
                break

    # ========================================
    #         EVENTOS Y CONTROLES
    # ========================================

    RUNGAME = handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME)

    keys_pressed = pygame.key.get_pressed()
    handle_player_controls(player, keys_pressed)

    # Dibuja todo
    gameWindowUpdating(config.GAMESCREEN, player, playerBullets, asteroidObjects, assets['bgImg'], assets['heartImg'])
    config.CLOCK.tick(config.FPS)

pygame.quit()
sys.exit()
