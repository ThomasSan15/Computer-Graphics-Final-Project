# ==============================
#   MANEJO DE EVENTOS
# ==============================

import pygame
from src import config
from src.classes.bullet import Bullet
from src.game_logic import generate_asteroids, resetAfterLosingALife
from src.utils.general import saveTopScoreFile
from pygame import Vector2


# Variable global para el controlador de gestos
hand_controller = None


def initialize_hand_controller():
    """Inicializa el controlador de gestos de mano"""
    global hand_controller
    try:
        from src.hand_gesture_controller import HandGestureController
        hand_controller = HandGestureController(smoothing_window=3, debug=False)
        print("✓ Controlador de mano inicializado correctamente")
        return True
    except Exception as e:
        print(f"✗ Error al inicializar controlador de mano: {e}")
        return False


def handle_events(player, playerBullets, asteroidObjects, assets, RUNGAME):
    """Maneja todos los eventos del juego"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            # Reiniciar tras Game Over
            if config.GAMEOVER and event.key == pygame.K_TAB:
                resetAfterLosingALife(player, asteroidObjects, playerBullets)
                config.STAGE = 1
                config.LIVES = 3
                config.SCORE = 0
                config.GAMEOVER = False
                generate_asteroids(asteroidObjects, __import__('src.classes.asteroid', fromlist=['Asteroid']).Asteroid, assets)

    return RUNGAME


def update_hand_gesture_control(player, playerBullets, assets):
    """
    Procesa el control de gestos de mano y actualiza la rotación de la nave
    También maneja el disparo automático
    """
    global hand_controller
    
    if hand_controller is None:
        return
    
    # Procesar frame de la cámara
    result = hand_controller.process_frame()
    
    # Si la calibración está completa, usar el ángulo de rotación
    if result['calibrated'] and result['hand_detected']:
        # Calcular el ángulo de rotación deseado
        target_rotation = -result['ship_rotation']  # INVERTIDO
        
        # Obtener ángulo actual de la nave
        current_angle = player.direction.angle_to(Vector2(0, -1))
        
        # Calcular diferencia angular
        angle_diff = target_rotation - current_angle
        
        # Normalizar diferencia a rango [-180, 180]
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
        
        # Aplicar rotación suave (limitar el cambio por frame)
        max_rotation_per_frame = 8  # Balance entre responsividad y control
        if abs(angle_diff) > max_rotation_per_frame:
            rotation_delta = max_rotation_per_frame if angle_diff > 0 else -max_rotation_per_frame
        else:
            rotation_delta = angle_diff
        
        # Aplicar rotación
        player.direction.rotate_ip(rotation_delta)
        
        # Controlar movimiento con posición de la mano
        # hand_x = 0 (izquierda), 0.5 (centro), 1 (derecha)
        # hand_y = 0 (arriba), 0.5 (centro), 1 (abajo)
        
        hand_x = result['hand_x']
        hand_y = result['hand_y']
        
        # Calcular vectores de dirección
        forward = player.direction
        right_vector = Vector2(-player.direction.y, player.direction.x)
        
        # Extraer componentes actuales
        forward_vel = player.velocity.dot(forward)
        lateral_vel = player.velocity.dot(right_vector)
        
        # Controlar movimiento vertical (forward/backward)
        if hand_y < 0.4:
            forward_vel = player.speed * 2
        elif hand_y > 0.6:
            forward_vel = -player.speed * 2
        else:
            forward_vel *= 0.9  # Desacelerar suavemente
        
        # Controlar movimiento horizontal (izquierda/derecha)
        if hand_x < 0.4:
            lateral_vel = -player.speed * 1.5
        elif hand_x > 0.6:
            lateral_vel = player.speed * 1.5
        else:
            lateral_vel *= 0.9  # Desacelerar suavemente
        
        # Reconstruir velocidad
        player.velocity = forward * forward_vel + right_vector * lateral_vel
        
        # Limitar velocidad máxima
        if player.velocity.length() > 4:
            player.velocity.scale_to_length(4)
    
    # Disparo automático continuo (cada 6 frames aproximadamente)
    config.FRAME_COUNTER = getattr(config, 'FRAME_COUNTER', 0) + 1
    if config.FRAME_COUNTER % 6 == 0:
        playerBullets.append(Bullet(player.pos, player.direction))
        assets['shootSound'].play()


def handle_player_controls(player, keys_pressed):
    """
    Maneja los controles de movimiento del jugador
    Ahora solo controla aceleración (rotación es por visión)
    """
    # Avanzar
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        player.accelerate()

    # Retroceso (inverso)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        player.velocity -= player.direction * player.speed
        if player.velocity.length() > 4:
            player.velocity.scale_to_length(4)


def cleanup_hand_controller():
    """Libera los recursos del controlador de mano"""
    global hand_controller
    if hand_controller is not None:
        hand_controller.release()
        hand_controller = None
