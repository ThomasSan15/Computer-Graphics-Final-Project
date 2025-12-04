import sys
import os
import pygame
from pygame import Vector2
import traceback


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
from src.rendering import gameWindowUpdating, drawStartScreen, drawAsteroidHitScreen
from src.event_handler import handle_events, handle_player_controls
from src.hand_control import HandController

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

# Inicialización del control por mano (opcional)
hand_controller = HandController(config.SCREENWIDTH, config.SCREENHEIGHT)
if hand_controller.is_available:
    started = hand_controller.start()
    if started:
        print('Hand control initialized')
    else:
        print('Hand control not available')
else:
    print('Hand control not available')

# Disparo automático: intervalo entre balas (ms)
shot_interval_ms = 220
last_shot_time = 0

# ==============================
#      BUCLE PRINCIPAL
# ==============================

RUNGAME = True
while RUNGAME:
    try:
        # Pantalla de inicio
        if not config.GAME_STARTED:
            drawStartScreen(config.GAMESCREEN)
            RUNGAME = handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME, hand_controller)
            config.CLOCK.tick(config.FPS)
            continue

        # Pantalla de impacto con asteroide
        if config.HIT_BY_ASTEROID:
            drawAsteroidHitScreen(config.GAMESCREEN)
            RUNGAME = handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME, hand_controller)
            config.HIT_TIMER -= 1
            if config.HIT_TIMER <= 0:
                config.HIT_BY_ASTEROID = False
            config.CLOCK.tick(config.FPS)
            continue

        if not config.GAMEOVER:

            # Cambiar etapa si no quedan asteroides
            if check_asteroidCount_increase_stage(asteroidObjects):
                generate_asteroids(asteroidObjects, Asteroid, assets)

            # -------------------------
            # Movimiento de jugador
            # -------------------------
            # Actualizar control por mano si está disponible
            if hand_controller is not None and hand_controller.is_available:
                try:
                    hand_controller.update(player)
                except Exception:
                    pass

            player.move()

            # -------------------------
            # Disparo automático continuo (sin gesto)
            # -------------------------
            now = pygame.time.get_ticks()
            if now - last_shot_time >= shot_interval_ms:
                # Solo disparar si el juego está en progreso y no estamos mostrando
                # la pantalla de impacto
                if config.GAME_STARTED and not config.HIT_BY_ASTEROID:
                    playerBullets.append(Bullet(player.pos, player.direction))
                    try:
                        assets['shootSound'].play()
                    except Exception:
                        pass
                last_shot_time = now

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
                    if hasattr(bullet, 'bulletRect') and bullet.bulletRect.colliderect(asteroidObject.imgRect):
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

        RUNGAME = handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME, hand_controller)

        if not config.GAME_STARTED or config.HIT_BY_ASTEROID:
            continue

        keys_pressed = pygame.key.get_pressed()
        handle_player_controls(player, keys_pressed)

        # Dibuja todo
        if config.HIT_BY_ASTEROID:
            drawAsteroidHitScreen(config.GAMESCREEN)
        elif config.GAME_STARTED:
            gameWindowUpdating(config.GAMESCREEN, player, playerBullets, asteroidObjects, assets['bgImg'], assets['heartImg'])
        else:
            drawStartScreen(config.GAMESCREEN)
        config.CLOCK.tick(config.FPS)
    except Exception:
        tb = traceback.format_exc()
        print(tb)
        try:
            with open('crash_log.txt', 'a') as f:
                f.write('\n--- Crash ---\n')
                f.write(tb)
        except Exception:
            pass
        RUNGAME = False

# Limpieza recursos de cámara / MediaPipe si se activó control por mano
if hand_controller is not None and getattr(hand_controller, 'is_available', False):
    try:
        hand_controller.stop()
    except Exception:
        pass

pygame.quit()
sys.exit()