<<<<<<< HEAD
# Tanda-de-Penales-Mundial
=======
# Tanda de Penales — Mundial 2026

Mini-juego de penales desarrollado en Python y Pygame.

## Requisitos
- Python 3.8 o superior
- Pygame

## Instalación
1. Instala Python 3.8+.
2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install pygame
   ```

## Ejecución
```bash
python main.py
```

## Controles
- `IZQUIERDA` / `DERECHA`: navegar en menús y elegir zona de tiro
- `ENTER`: confirmar selección en el menú
- `ESPACIO`: disparar penal en el juego
- `R`: reiniciar cuando la tanda termine
- `ESC`: volver atrás en el menú

## Arquitectura de módulos
- `main.py`: inicializa Pygame, la ventana, el menú de selecciones y el ciclo principal.
- `menu.py`: controla la selección de equipos con banderas generadas en código.
- `juego.py`: maneja el estado del juego, los disparos, la animación y los equipos seleccionados.
- `portero.py`: lógica adaptativa del portero que aprende de las elecciones del jugador.
- `ui.py`: dibuja el menú, el campo, el arco, el portero, la pelota y la interfaz.
- `animacion.py`: proporciona curvas de aceleración y la interpolación con ease-in/ease-out.
- `tests.py`: pruebas automáticas con `SDL_VIDEODRIVER=dummy`.

## Pruebas automáticas
Ejecuta las pruebas con:
```bash
python tests.py
```

Si ves problemas al correr la ventana en un entorno sin pantalla, usa:
```bash
set SDL_VIDEODRIVER=dummy
python tests.py
```

## Evidencia de vibecoding y prompts
Se usaron prompts claros y progresivos para construir y refinar la interfaz y el comportamiento del juego.

Ejemplos de prompts utilizados:
1. "Organiza el HUD en tres paneles independientes" — se pidió estructurar la interfaz en componentes separados para evitar superposición y mejorar la claridad visual: marcador, equipo y controles.
2. "Mueve el marcador al área de selección de equipos y haz el panel de instrucciones más legible" — se solicitó reorganizar la disposición del marcador y refinar el panel de instrucciones con un diseño más limpio.
3. "Mejora solamente la sección de zona activa" — se indicó abordar únicamente el bloque de zona activa para optimizar su presentación sin modificar el resto de la UI.

Para cada prompt se ajustó el diseño y se validó el resultado en el código. La iteración permitió resolver problemas de superposición del HUD, visibilidad de controles y claridad de la interfaz.

## Iteración y mejoras
- Se realizó una mejora visual del campo, la portería y la animación del portero.
- Se separaron los paneles de HUD en marcador, equipos y controles.
- Se corrigió la posición del marcador para que no tape la portería.
- Se mejoró el panel de instrucciones y la caja de "Zona activa" para que sean más legibles.

## Validación
Se probó el código con las siguientes acciones:
- Ejecución normal del juego en Pygame.
- Pruebas automáticas con SDL dummy para evitar abrir ventana de video.

Prueba ejecutada:
```bash
set SDL_VIDEODRIVER=dummy
py -3 tests.py
```
Resultado:
- 4 pruebas ejecutadas, todas OK.

## Reflexión
- Aprendí a usar IA como asistente para iterar rápidamente la interfaz y ajustar el comportamiento del juego.
- Ventajas del vibecoding: acelera la creación, permite refinar instrucciones puntuales y ayuda a visualizar mejoras de UI.
- Límites: es necesario revisar y entender el código generado para evitar cambios incorrectos o superposiciones visuales.
- Comprendo bien la estructura del juego, el ciclo principal, la selección de equipos y el renderizado en `ui.py`. Necesito reforzar el diseño de prompts más exactos y la depuración avanzada de Pygame cuando aparecen detalles visuales finos.
>>>>>>> ea1ee89 (Juego de tanda de penales)
