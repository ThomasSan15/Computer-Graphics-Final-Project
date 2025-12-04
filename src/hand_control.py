# Módulo para control por mano usando MediaPipe y OpenCV
# El módulo intenta inicializar la cámara y MediaPipe; si no están
# disponibles, HandController.is_available será False y no hará nada.

import math
from pygame import Vector2

try:
    import cv2
    import mediapipe as mp
    _HAS_MEDIAPIPE = True
except Exception:
    _HAS_MEDIAPIPE = False


class HandController:
    """Controla la lectura de la cámara y actualiza la posición/dirección del jugador.

    Uso:
        hc = HandController(screen_w, screen_h)
        if hc.is_available:
            hc.start()
        inside game loop: hc.update(player)
        al salir: hc.stop()
    """

    def __init__(self, screen_w, screen_h, max_num_hands=1, detection_conf=0.6,
                 pos_alpha=0.05, dir_alpha=1):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos_alpha = pos_alpha
        self.dir_alpha = dir_alpha
        self.max_num_hands = max_num_hands
        self.detection_conf = detection_conf

        self.is_available = _HAS_MEDIAPIPE
        self.cap = None
        self.hands = None
        self.mp_draw = None
        self.last_hand_pos = None
        self.last_hand_dir = None
        self.hand_rotation_flip = 1

    def start(self):
        if not self.is_available:
            return False
        try:
            self.cap = cv2.VideoCapture(0)
            mp_hands = mp.solutions.hands
            self.hands = mp_hands.Hands(max_num_hands=self.max_num_hands,
                                        min_detection_confidence=self.detection_conf)
            self.mp_draw = mp.solutions.drawing_utils
            # Se inicializan vectores al centro
            from pygame import Vector2
            self.last_hand_pos = Vector2(self.screen_w//2, self.screen_h//2)
            self.last_hand_dir = Vector2(0, -1)
            return True
        except Exception:
            self.is_available = False
            return False

    def stop(self):
        try:
            if self.hands is not None:
                self.hands.close()
            if self.cap is not None:
                self.cap.release()
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass
        except Exception:
            pass

    def _lerp_angle(self, a, b, t):
        diff = (b - a + math.pi) % (2 * math.pi) - math.pi
        return a + diff * t

    def update(self, player):
        """Lee un frame de la cámara y, si detecta mano, actualiza
        player.pos y player.direction. Retorna True si se detectó mano.
        """
        if not self.is_available or self.cap is None or self.hands is None:
            return False

        ret, frame = self.cap.read()
        if not ret:
            return False

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            lm = hand_landmarks.landmark

            # --- POSICIÓN: punta del pulgar (landmark 4) ---
            thumb_tip = lm[4]
            measured_x = thumb_tip.x * self.screen_w
            measured_y = thumb_tip.y * self.screen_h
            measured_pos = Vector2(measured_x, measured_y)

            # Suavizado exponencial
            self.last_hand_pos = self.last_hand_pos * (1.0 - self.pos_alpha) + measured_pos * self.pos_alpha
            player.pos = Vector2(self.last_hand_pos)
            player.imgRect.x = int(player.pos[0] - player.width // 2)
            player.imgRect.y = int(player.pos[1] - player.height // 2)

            # Determinar orientación (handedness) si está disponible
            if hasattr(results, 'multi_handedness') and results.multi_handedness:
                try:
                    handedness_label = results.multi_handedness[0].classification[0].label
                    if handedness_label == 'Right':
                        self.hand_rotation_flip = -1
                    else:
                        self.hand_rotation_flip = 1
                except Exception:
                    pass

            # --- ROTACIÓN: wrist (0) -> thumb_tip (4) ---
            wrist = lm[0]
            vx = thumb_tip.x - wrist.x
            vy = thumb_tip.y - wrist.y
            measured_dir = Vector2(vx, -vy)

            if measured_dir.length() > 1e-6:
                measured_angle = math.atan2(measured_dir.y, measured_dir.x)
                # Corregimos el ángulo para que apunte en la misma convención
                # que usa el juego original (se invierte el ángulo medido).
                corrected_angle = -measured_angle

                try:
                    last_angle = math.atan2(self.last_hand_dir.y, self.last_hand_dir.x)
                except Exception:
                    last_angle = corrected_angle

                mixed_angle = self._lerp_angle(last_angle, corrected_angle, self.dir_alpha)
                new_dir = Vector2(math.cos(mixed_angle), math.sin(mixed_angle))
                self.last_hand_dir = Vector2(new_dir)
                player.direction = Vector2(new_dir)

            return True

        return False
