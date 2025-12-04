# Asteroids — Proyecto Final (Computer Graphics)

Versión en Python del clásico juego "Asteroids". Este repositorio contiene una implementación hecha con `pygame`. Incluye soporte opcional de control por movimiento de manos mediante MediaPipe + OpenCV.

---

**Características principales**

- Juego estilo "Asteroids": nave, asteroides que se dividen, etapas y vidas.
- Modularización en varios módulos: assets, lógica, rendering, eventos y clases.
- Control por teclado y control opcional por movimiento de manos (MediaPipe + OpenCV).
- Auto-disparo configurable, sonidos y animaciones de asteroides.
- Manejo de pantalla de inicio, pantalla de impacto y record de puntaje.

---

**Requisitos**

- Python 3.10+ (no se asegura el soporte en versiones posteriores para control por cámara)
- Paquetes Python:
	- pygame
	- mediapipe (opcional, sólo si usarás control por mano)
	- opencv-python (opcional, sólo si usarás control por mano)

Recomendado usar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # zsh / bash
pip install -r requirements.txt  # si tienes un requirements, o instala manualmente
pip install pygame
pip install mediapipe opencv-python  # opcional para control por mano
```

Si no quieres instalar MediaPipe/OpenCV, el juego funcionará sólo con controles de teclado.

---

**Ejecutar el juego**

En la raíz del proyecto:

```bash
python3 main.py
```

Controles básicos:

- `SPACE`: iniciar juego / disparar
- `LEFT` / `A`: rotar a la izquierda
- `RIGHT` / `D`: rotar a la derecha
- `UP` / `W`: acelerar (propulsor)
- `DOWN` / `S`: retroceder
- `R`: invertir/ajustar la rotación del control por mano (toggle)
- `TAB`: reiniciar después de Game Over
- `ESC`: salir

---

**Estructura del repositorio**

- `main.py` — Entrada principal: inicializa el juego, carga assets, crea objetos y ejecuta el bucle principal.
- `TopScoreFile.txt` — Archivo con el record (mejor puntaje).
- `assets/` — Imágenes, sprites y sonidos.
- `src/` — Código modular:
	- `config.py` — Configuración y estado global del juego (FPS, dimensiones, flags).
	- `assets_loader.py` — Funciones para cargar imágenes y sonidos.
	- `game_logic.py` — Lógica independiente del render (generación de asteroides, reinicios, conteos).
	- `rendering.py` — Funciones encargadas de dibujar la escena y pantallas especiales.
	- `event_handler.py` — Mapeo de eventos de teclado y manejo de entrada.
	- `hand_control.py` — Encapsula MediaPipe + OpenCV y actualiza `Player` con posición/rotación por mano.
	- `classes/` — Clases del juego:
		- `player.py`, `bullet.py`, `asteroid.py`
	- `utils/` — Utilidades generales (carga de imágenes, texto, archivos de score).

---

**Control por mano (detalle técnico)**

El módulo `src/hand_control.py` expone `HandController`, que realiza:

- Inicialización de la cámara con `cv2.VideoCapture` y del detector `mediapipe.solutions.hands`.
- En cada frame detecta landmarks y usa la punta del pulgar (landmark 4) para determinar la posición de la nave en pantalla.
- Usa el vector muñeca (landmark 0) → punta del pulgar para calcular la dirección/ángulo apuntado.
- Aplica suavizado exponencial a la posición (`pos_alpha`) y suavizado/interpolación angular (`dir_alpha`) para reducir temblor y saltos.
- `hand_rotation_flip` permite invertir la dirección de rotación (basado en la clasificación de mano, y también toggle con `R`).
- Si la cámara o MediaPipe no están disponibles, `HandController.is_available` es False y el juego usa sólo control por teclado.

Parámetros relevantes:

- `pos_alpha` (por defecto 0.35): suavizado de posición — mayor = más reactivo, menor = más estable.
- `dir_alpha` (por defecto 0.5): suavizado angular — controla rapidez con que la nave gira para igualar la mano.

---

**Configuración y personalización**

- Variables globales en `src/config.py` (pantalla, FPS, `OBJECT_SPEED`, `OBJECT_ROTATION_SPEED`) son el primer lugar para ajustar comportamiento del juego.
- `shot_interval_ms` en `main.py` controla el intervalo de auto-disparo.
- Puedes exponer `pos_alpha` y `dir_alpha` moviéndolos a `config.py` para ajustarlos fácilmente.

---

**Depuración y logs**

- Si el juego falla, el `main.py` captura excepciones no manejadas y escribe un `crash_log.txt` con el traceback en la raíz del proyecto.
- Para ver el log:

```bash
cat crash_log.txt
```
--- 

**Créditos y origen**

Proyecto desarrollado como trabajo final del curso de Computación Gráfica.

**Desarrolladores**

<div style="display:flex; gap:20px; align-items:center;">
	<a href="https://github.com/pablomarin-utp" style="text-decoration:none; color:inherit; text-align:center;">
		<img src="https://github.com/pablomarin-utp.png" width="64" height="64" alt="pablomarin-utp" style="border-radius:8px; display:block; margin:0 auto 6px;">
		<div style="font-weight:600;">pablomarin-utp</div>
	</a>

	<a href="https://github.com/ThomasSan15" style="text-decoration:none; color:inherit; text-align:center;">
		<img src="https://github.com/ThomasSan15.png" width="64" height="64" alt="ThomasSan15" style="border-radius:8px; display:block; margin:0 auto 6px;">
		<div style="font-weight:600;">ThomasSan15</div>
	</a>

	<a href="https://github.com/Juan-Garcia16" style="text-decoration:none; color:inherit; text-align:center;">
		<img src="https://github.com/Juan-Garcia16.png" width="64" height="64" alt="Juan-Garcia16" style="border-radius:8px; display:block; margin:0 auto 6px;">
		<div style="font-weight:600;">Juan-Garcia16</div>
	</a>
</div>


