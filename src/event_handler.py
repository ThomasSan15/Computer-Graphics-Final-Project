# ==============================
#   MANEJO DE EVENTOS
# ==============================

import pygame
from src import config
from src.classes.bullet import Bullet
from src.game_logic import generate_asteroids, resetAfterLosingALife
from src.utils.general import saveTopScoreFile


def handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME, hand_controller=None):
    """Maneja todos los eventos del juego"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            # Continuar después de impacto con asteroide
            if config.HIT_BY_ASTEROID and event.key == pygame.K_SPACE:
                config.HIT_BY_ASTEROID = False
                config.HIT_TIMER = 0
                return RUNGAME

            # Iniciar juego desde pantalla de inicio
            if not config.GAME_STARTED and event.key == pygame.K_SPACE:
                config.GAME_STARTED = True
                pygame.mixer.music.play(-1)  # -1 para reproducir en loop infinito
                return RUNGAME

            # Disparo
            if config.GAME_STARTED and not config.HIT_BY_ASTEROID and event.key == pygame.K_SPACE:
                playerBullets.append(Bullet(player.pos, player.direction))
                assets['shootSound'].play()

            # Toggle para invertir rotación de mano
            if event.key == pygame.K_r and hand_controller is not None:
                try:
                    hand_controller.hand_rotation_flip *= -1
                    print(f'hand_rotation_flip = {hand_controller.hand_rotation_flip}')
                except Exception:
                    pass

            # Reiniciar tras Game Over
            if config.GAMEOVER and event.key == pygame.K_TAB:
                resetAfterLosingALife(player, asteroidObjects, playerBullets)
                config.STAGE = 1
                config.LIVES = 3
                config.SCORE = 0
                config.GAMEOVER = False
                config.GAME_STARTED = True
                config.HIT_BY_ASTEROID = False
                config.HIT_TIMER = 0
                pygame.mixer.music.play(-1)
                generate_asteroids(asteroidObjects, __import__('src.classes.asteroid', fromlist=['Asteroid']).Asteroid, assets)

    return RUNGAME


def handle_player_controls(player, keys_pressed):
    """Maneja los controles de movimiento del jugador"""
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        player.rotation(-1)
    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        player.rotation(1)

    # Avanzar
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        player.accelerate()

    # Retroceso (inverso)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        player.velocity -= player.direction * player.speed
        if player.velocity.length() > 4:
            player.velocity.scale_to_length(4)
