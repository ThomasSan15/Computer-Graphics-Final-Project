# ==============================
#   MANEJO DE EVENTOS
# ==============================

import pygame
from src import config
from src.classes.bullet import Bullet
from src.game_logic import generate_asteroids, resetAfterLosingALife
from src.utils.general import saveTopScoreFile


def handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME):
    """Maneja todos los eventos del juego"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            # Disparo
            if event.key == pygame.K_SPACE:
                playerBullets.append(Bullet(player.pos, player.direction))
                assets['shootSound'].play()

            # Reiniciar tras Game Over
            if config.GAMEOVER and event.key == pygame.K_TAB:
                resetAfterLosingALife(player, asteroidObjects, playerBullets)
                config.STAGE = 1
                config.LIVES = 3
                config.SCORE = 0
                config.GAMEOVER = False
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
