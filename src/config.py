# ==============================
#   CONFIGURACION DEL JUEGO
# ==============================

import pygame

# Dimensiones de pantalla
SCREENWIDTH = 1200
SCREENHEIGHT = 700

# Configuración de objetos
OBJECT_ROTATION_SPEED = 3
OBJECT_SPEED = 0.10

# Estado inicial del juego
STAGE = 0
LIVES = 3
GAMEOVER = False
SCORE = 0
TOPSCORE = 0
GAME_STARTED = False  # False = pantalla de inicio, True = juego en progreso
HIT_BY_ASTEROID = False  # True cuando nos golpea un asteroide
HIT_TIMER = 0  # Contador para mostrar pantalla de impacto durante 3 segundos

# Clock y FPS
CLOCK = pygame.time.Clock()
FPS = 60

# Pantalla principal
GAMESCREEN = None
