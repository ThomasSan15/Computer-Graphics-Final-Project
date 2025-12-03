# ==============================
#   CONTROL DE GESTO DE MANO
# ==============================

import mediapipe as mp
import numpy as np
from collections import deque
from src import config


class HandGestureController:
    """Controlador de gestos de mano usando MediaPipe Hands"""

    def __init__(self, smoothing_window=5, debug=False):
        """
        Inicializa el controlador de gestos de mano
        
        Args:
            smoothing_window: Número de frames para suavizar el ángulo (reduce jitter)
            debug: Si True, muestra información de depuración
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Captura de video usando mediapipe
        self.cap = None
        self.camera_initialized = False
        self.cv2_available = False
        
        try:
            import cv2
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.camera_initialized = True
                self.cv2_available = True
                print("✓ OpenCV disponible - usando captura con cv2")
        except ImportError:
            print("⚠ OpenCV no disponible - intentando con alternativa")
            self.cv2_available = False
            self.camera_initialized = False
        
        # Suavizado de ángulos (prevenir jitter)
        self.smoothing_window = smoothing_window
        self.angle_history = deque(maxlen=smoothing_window)
        
        # Ángulo neutral (posición inicial)
        self.neutral_angle = None
        self.debug = debug
        
        # Calibración
        self.is_calibrated = False
        self.calibration_frames = 0
        self.calibration_threshold = 2  # Solo 2 frames para calibrar - tiempo real

    def calibrate_neutral_position(self):
        """Calibra la posición neutral de la mano (apuntando hacia adelante)"""
        if self.calibration_frames < self.calibration_threshold:
            self.calibration_frames += 1
            return False
        
        if len(self.angle_history) > 0:
            # Promediar los últimos ángulos para establecer neutral
            self.neutral_angle = np.mean(list(self.angle_history))
            self.is_calibrated = True
            print(f"✓ Calibración completada. Ángulo neutral: {self.neutral_angle:.2f}°")
            if self.debug:
                print(f"   Ahora gira la mano para controlar la nave")
            return True
        return False

    def calculate_thumb_angle(self, hand_landmarks, frame_height, frame_width):
        """
        Calcula el ángulo de rotación de la mano en el plano XZ
        
        Returns:
            angle: Ángulo en grados (positivo = derecha, negativo = izquierda)
        """
        if hand_landmarks is None:
            return None
        
        try:
            # Usar múltiples puntos para calcular rotación de la mano
            # Landmark 0: muñeca
            # Landmark 5: base del índice
            # Landmark 9: base del corazón
            # Landmark 17: base del meñique
            
            wrist = hand_landmarks[0]
            middle = hand_landmarks[9]
            
            # Convertir a coordenadas de píxeles
            wrist_x = wrist.x * frame_width
            wrist_y = wrist.y * frame_height
            wrist_z = wrist.z
            
            middle_x = middle.x * frame_width
            middle_y = middle.y * frame_height
            middle_z = middle.z
            
            # Vector desde muñeca a corazón (eje de la mano)
            hand_vector = np.array([middle_x - wrist_x, middle_y - wrist_y])
            
            # Evitar división por cero
            if np.linalg.norm(hand_vector) < 1:
                return None
            
            # Calcular ángulo respecto al eje vertical (arriba)
            # atan2(x, y) donde y es hacia arriba (negativo en pantalla)
            angle_rad = np.arctan2(hand_vector[0], -hand_vector[1])
            angle_deg = np.degrees(angle_rad)
            
            # Normalizar a rango [-180, 180]
            if angle_deg > 180:
                angle_deg -= 360
            elif angle_deg < -180:
                angle_deg += 360
            
            return angle_deg
        except:
            return None

    def get_smoothed_angle(self):
        """Retorna el ángulo suavizado del historial"""
        if len(self.angle_history) == 0:
            return 0
        return np.mean(list(self.angle_history))

    def get_ship_rotation_angle(self):
        """
        Calcula el ángulo de rotación de la nave
        
        Returns:
            rotation_angle: Ángulo en grados (1:2 ratio con el pulgar)
        """
        if not self.is_calibrated or len(self.angle_history) == 0:
            return 0
        
        current_smoothed = self.get_smoothed_angle()
        
        # Diferencia respecto a posición neutral
        angle_diff = current_smoothed - self.neutral_angle
        
        # Aplicar ratio 1:2 (pulgar 1° = nave 2°)
        ship_rotation = angle_diff * 2
        
        return ship_rotation

    def process_frame(self):
        """
        Procesa un frame de la cámara y retorna información de la mano
        """
        if not self.camera_initialized or self.cap is None or not self.cv2_available:
            return {
                'hand_detected': False,
                'thumb_angle': 0,
                'ship_rotation': 0,
                'hand_x': 0.5,
                'hand_y': 0.5,
                'calibrated': self.is_calibrated
            }
        
        try:
            import cv2
            ret, frame = self.cap.read()
            if not ret:
                return {
                    'hand_detected': False,
                    'thumb_angle': 0,
                    'ship_rotation': 0,
                    'hand_x': 0.5,
                    'hand_y': 0.5,
                    'calibrated': self.is_calibrated
                }
            
            # Voltear frame para efecto espejo
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            
            # Convertir a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar manos
            results = self.hands.process(frame_rgb)
            
            thumb_angle = 0
            hand_detected = False
            hand_x = 0.5  # Centro por defecto
            hand_y = 0.5
            
            # Si se detectó una mano
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
                hand_detected = True
                hand_landmarks = results.multi_hand_landmarks[0].landmark
                
                # Obtener posición de la muñeca (centro de la mano)
                wrist = hand_landmarks[0]
                hand_x = wrist.x  # Normalizado 0-1
                hand_y = wrist.y  # Normalizado 0-1
                
                # Calcular ángulo del pulgar
                thumb_angle = self.calculate_thumb_angle(
                    hand_landmarks, frame_height, frame_width
                )
                
                if thumb_angle is not None:
                    self.angle_history.append(thumb_angle)
                    
                    if self.debug:
                        print(f"Pulgar: {thumb_angle:.1f}° | Pos: ({hand_x:.2f}, {hand_y:.2f}) | Calibrado: {self.is_calibrated}")
                    
                    # Calibración automática
                    if not self.is_calibrated:
                        self.calibrate_neutral_position()
            
            ship_rotation = self.get_ship_rotation_angle()
            
            return {
                'hand_detected': hand_detected,
                'thumb_angle': thumb_angle,
                'ship_rotation': ship_rotation,
                'hand_x': hand_x,
                'hand_y': hand_y,
                'calibrated': self.is_calibrated
            }
        except Exception as e:
            if self.debug:
                print(f"Error procesando frame: {e}")
                import traceback
                traceback.print_exc()
            return {
                'hand_detected': False,
                'thumb_angle': 0,
                'ship_rotation': 0,
                'hand_x': 0.5,
                'hand_y': 0.5,
                'calibrated': self.is_calibrated
            }

    def release(self):
        """Libera recursos de la cámara y MediaPipe"""
        try:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
        except:
            pass
        
        try:
            self.hands.close()
        except:
            pass
