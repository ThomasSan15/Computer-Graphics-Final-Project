# ==============================
#   RENDERIZADO DE PANTALLA
# ==============================

import pygame
from src import config
from src.utils.general import textScreen


def drawStartScreen(GAMESCREEN):
    """Dibuja la pantalla de inicio"""
    shadow, titleText = textScreen("ASTEROIDS", 80, (255, 200, 50))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - titleText.get_width() // 2 - 3, 80))
    GAMESCREEN.blit(titleText, (config.SCREENWIDTH // 2 - titleText.get_width() // 2, 80))
    
    shadow, startText = textScreen("Press SPACE to Start", 36, (150, 255, 150))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - startText.get_width() // 2 - 2, config.SCREENHEIGHT // 2))
    GAMESCREEN.blit(startText, (config.SCREENWIDTH // 2 - startText.get_width() // 2, config.SCREENHEIGHT // 2))
    
    shadow, bestText = textScreen(f"Best Score: {config.TOPSCORE}", 24, (0, 255, 255))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - bestText.get_width() // 2 - 1, config.SCREENHEIGHT - 150))
    GAMESCREEN.blit(bestText, (config.SCREENWIDTH // 2 - bestText.get_width() // 2, config.SCREENHEIGHT - 150))
    
    pygame.display.update()


def drawAsteroidHitScreen(GAMESCREEN):
    """Dibuja la pantalla de impacto con asteroide"""
    shadow, hitText = textScreen("¡GOLPEADO POR ASTEROIDE!", 50, (255, 50, 50))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - hitText.get_width() // 2 - 3, config.SCREENHEIGHT // 2 - 100))
    GAMESCREEN.blit(hitText, (config.SCREENWIDTH // 2 - hitText.get_width() // 2, config.SCREENHEIGHT // 2 - 100))
    
    if config.LIVES > 0:
        shadow, continueText = textScreen("Press SPACE to continue...", 30, (150, 255, 150))
        GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - continueText.get_width() // 2 - 2, config.SCREENHEIGHT // 2 + 50))
        GAMESCREEN.blit(continueText, (config.SCREENWIDTH // 2 - continueText.get_width() // 2, config.SCREENHEIGHT // 2 + 50))
    
    shadow, livesText = textScreen(f"Vidas restantes: {config.LIVES}", 28, (0, 255, 255))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - livesText.get_width() // 2 - 1, config.SCREENHEIGHT - 100))
    GAMESCREEN.blit(livesText, (config.SCREENWIDTH // 2 - livesText.get_width() // 2, config.SCREENHEIGHT - 100))
    
    pygame.display.update()


def gameWindowUpdating(GAMESCREEN, player, playerBullets, asteroidObjects, BGIMG, heartImg):
    """Dibuja todos los elementos en pantalla y actualiza el frame"""
    GAMESCREEN.blit(BGIMG, (0, 0))

    if not config.GAMEOVER:
        for bullet in playerBullets:
            bullet.draw(GAMESCREEN)

        for asteroidObject in asteroidObjects:
            asteroidObject.draw(GAMESCREEN)
            asteroidObject._animate_image()

        player.draw(GAMESCREEN)

    # ♥ Dibuja vidas con corazones PNG
    for i in range(config.LIVES):
        GAMESCREEN.blit(heartImg, (40 + i * 35, 25))

    # Texto Score y Best Score
    shadow, score = textScreen(f"SCORE {config.SCORE}", 32, (255, 230, 0))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH - 200, 25))
    GAMESCREEN.blit(score, (config.SCREENWIDTH - 200, 25))

    shadow, topscore = textScreen(f"BEST {config.TOPSCORE}", 28, (0, 255, 255))
    GAMESCREEN.blit(shadow, (config.SCREENWIDTH - 200, 60))
    GAMESCREEN.blit(topscore, (config.SCREENWIDTH - 200, 60))

    # ★ Etapa
    shadow, stage = textScreen(f"STAGE {config.STAGE}", 30, (140, 255, 140))
    GAMESCREEN.blit(shadow, (85, 85))
    GAMESCREEN.blit(stage, (85, 85))

    # Barra de progreso de asteroides restantes
    from src.game_logic import calculateTotalNumAsteroids
    numAsteroids = calculateTotalNumAsteroids(asteroidObjects)
    total = config.STAGE * 7
    barW = 200
    pygame.draw.rect(GAMESCREEN, (60, 60, 60), (25, 70, barW, 14), border_radius=10)
    if total > 0:
        pygame.draw.rect(GAMESCREEN, (80, 255, 80), (25, 70, barW * (numAsteroids / total), 14), border_radius=10)

    # Pantalla de Game Over
    if config.GAMEOVER:
        shadow, gameOverText = textScreen("GAME OVER! Press TAB to restart", 46, (255, 50, 50))
        GAMESCREEN.blit(shadow, (config.SCREENWIDTH // 2 - gameOverText.get_width() // 2 - 2, config.SCREENHEIGHT // 2 - 40))
        GAMESCREEN.blit(gameOverText, (config.SCREENWIDTH // 2 - gameOverText.get_width() // 2, config.SCREENHEIGHT // 2 - 40))

    pygame.display.update()
