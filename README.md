# Tanda de Penales — Mundial 2026

Mini-juego de penales desarrollado en Python y Pygame, con selección de equipos, portero adaptativo y sonido generado de forma procedural (sin archivos de audio externos).

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
- `IZQUIERDA` / `DERECHA`: navegar el menú de equipos, o cambiar la zona de tiro durante el partido
- `ENTER`: confirmar selección en el menú
- `ESPACIO`: disparar penal
- `ESC`: en el menú, retrocede de fase rival a jugador (o cierra el menú); durante el partido, vuelve a la pantalla de selección de equipos
- `R`: reiniciar la tanda (solo cuando ya terminó)

## Arquitectura de módulos
- `main.py`: inicializa Pygame, la ventana (1024x700), el bucle principal y los eventos de teclado. Genera los efectos de sonido de forma procedural con `array` y `math.sin` (silbato, gol, atajada, menú), sin depender de archivos de audio externos, y maneja con `try/except pygame.error` el caso en que el mixer no esté disponible.
- `menu.py`: maneja la selección de jugador y rival entre 8 selecciones reales del Mundial (Canadá, Brasil, México, España, Japón, Francia, Argentina, Marruecos), evitando que ambos elijan el mismo equipo.
- `juego.py`: estado de una tanda de 5 disparos: selección de zona, resultado del disparo (gol/atajada) y disparo de las animaciones de pelota y portero.
- `portero.py`: lógica adaptativa del portero, basada en un conteo acumulado de las elecciones históricas del jugador (ver limitación abajo).
- `animacion.py`: interpolación de posición con una curva de aceleración `ease_in_out_cubic`, usada para mover la pelota y el portero de forma suave durante cada disparo.
- `ui.py`: dibuja el campo, el estadio, el arco con red, el portero, la pelota, y un HUD separado en tres paneles (marcador, equipos, controles), además de la pantalla de selección de equipos.
- `tests.py`: 4 pruebas automáticas con `unittest`, ejecutadas con `SDL_VIDEODRIVER=dummy` para no requerir una ventana real.

## Pruebas automáticas
```bash
python tests.py
```
Si corres en un entorno sin pantalla:
```bash
set SDL_VIDEODRIVER=dummy
python tests.py
```

Las 4 pruebas verifican:
1. `test_juego_termina_despues_de_cinco_tiros`: que la tanda termina exactamente tras 5 disparos y que cada resultado registra una zona válida.
2. `test_portero_adaptativo_aumenta_probabilidad_para_zona_elegida`: que repetir una zona aumenta su probabilidad por encima de las otras dos.
3. `test_portero_elige_zona_con_pesos_adaptativos`: que, en 200 simulaciones, el portero efectivamente se lanza con más frecuencia hacia la zona reforzada (no solo en el cálculo de probabilidad, sino en el sorteo real).
4. `test_menu_selecciona_dos_equipos_distintos`: que el menú nunca asigna el mismo equipo a jugador y rival.

## Evidencia de vibecoding y prompts

Durante el desarrollo se emplearon al menos tres prompts distintos para orientar la implementación y los refinamientos.

1. Prompt de UI y organización del HUD
   - **Qué se pidió:** "Organiza el HUD en tres paneles independientes: marcador, equipos y controles. Que no se superponga con el campo ni tape información importante."
   - **Por qué se ajustó:** el diseño inicial amontonaba elementos cerca del arco. Se refinó para separar la información y mejorar la legibilidad.
   - **Cumplimiento en el código:** este prompt se cumple completamente.

2. Prompt de portero adaptativo
   - **Qué se pidió:** "En `portero.py`, cambia la elección de zona para que use `random.choices` con pesos adaptativos según cuántas veces el jugador eligió cada zona."
   - **Por qué se ajustó:** el portero aleatorio no ofrecía un desafío consistente. Se refinó para que el portero aprenda del patrón del jugador.
   - **Cumplimiento en el código:** este prompt se cumple parcialmente. El portero usa pesos adaptativos, pero no conserva únicamente las últimas 5 elecciones ni implementa un piso estricto del 15%.

3. Prompt de validación con pruebas automáticas
   - **Qué se pidió:** "En `tests.py`, añade una prueba que registre varias veces la misma zona del jugador y verifique que `portero.probabilidades()` aumenta la probabilidad de esa zona, y que `portero.elegir_zona()` la selecciona más seguido en una muestra."
   - **Por qué se ajustó:** era necesario validar con pruebas automáticas que la adaptación funciona en el código.
   - **Cumplimiento en el código:** este prompt se cumple completamente.
     
### Lógica del portero adaptativo

**1.**
> "En portero.py, el portero elige zona al azar (33% cada lado). Cámbialo para que 'aprenda': que registre las últimas 5 zonas del jugador y aumente la probabilidad de lanzarse hacia la zona que más se repite, en vez de elegir siempre al azar."

*Por qué se pidió:* el portero aleatorio no generaba ningún reto creciente; quería que reaccionara al patrón del jugador.

**2.**
> "El portero se está volviendo casi imbatible cuando el jugador repite zona. Pon un piso mínimo de 15% de probabilidad para cada zona, sin importar cuánto se repita una."

*Por qué se ajustó:* al probar repitiendo la misma zona varias veces, la probabilidad de esa zona subía mucho y dejaba las otras dos casi en cero, lo que hacía el juego injugable a la larga.

**3.**
> "Conecta el portero adaptativo en juego.py (reemplaza el random.choice por su elegir_zona()) y escribe una prueba en tests.py que simule 10 disparos a la misma zona y verifique con assert que su probabilidad subió."

*Por qué se pidió:* necesitaba confirmar que el aprendizaje afectaba el comportamiento real del juego, y tener una prueba automática en vez de validar jugando manualmente cada vez.

### Interfaz (HUD)

**4.** "Organiza el HUD en tres paneles independientes: marcador, equipos y controles, para evitar superposición y mejorar la claridad visual."

**5.** "Mueve el marcador al área de selección de equipos y haz el panel de instrucciones más legible."

**6.** "Mejora solamente la sección de zona activa, sin modificar el resto de la UI."

*Por qué se ajustó (4-6):* la primera versión del HUD tenía el marcador y los controles compitiendo por espacio visual cerca del arco; se separaron en paneles independientes (`_dibujar_puntos` y `_dibujar_ui` en `ui.py`) para que cada bloque de información tuviera su propio recuadro y no se solapara con el campo de juego.

## Iteración y mejoras
- Se separaron los paneles del HUD en marcador, equipos y controles (`ui.py`, métodos `_dibujar_puntos` y `_dibujar_ui`).
- Se agregó la animación de pelota y portero con curva de aceleración (`animacion.py`), en lugar de resolver el disparo de forma instantánea.
- Se implementó sonido procedural (sin archivos externos) para silbato, gol, atajada y navegación de menú.
- Se intentó agregar un piso mínimo de probabilidad al portero adaptativo (ver limitación abajo: quedó pendiente en la versión final).

## Validación
Se probó el código en tres niveles:
1. Ejecución normal del juego en Pygame, jugando varias tandas completas.
2. Pruebas automáticas (`tests.py`) con `SDL_VIDEODRIVER=dummy`, resultado: **4 pruebas ejecutadas, OK**.
3. Inspección manual de `portero.probabilidades()` para confirmar el comportamiento real del aprendizaje:

```python
from portero import Portero
p = Portero(semilla=99)
for _ in range(10):
    p.registrar_eleccion('derecha')
print(p.probabilidades())
# {'izquierda': 0.111, 'centro': 0.111, 'derecha': 0.778}
```

**Limitación identificada:** el piso mínimo de 15% solicitado en el prompt 2 **no llegó a implementarse** en la versión final de `portero.py`. Tras 10 disparos repetidos a la misma zona, las otras dos zonas caen a 11.1% cada una (por debajo del piso buscado), y en pruebas más extremas (30 disparos repetidos) caen hasta 4.8%. Además, `portero.py` no usa una ventana de las últimas 5 elecciones como se pidió en el prompt 1, sino un conteo acumulado de todo el historial de disparos del jugador. Ambos puntos quedan como mejoras pendientes para una siguiente iteración.

## Reflexión final
- Usar IA como asistente fue más efectivo para la parte mecánica (dibujar el HUD en paneles, generar tonos de audio, estructurar el bucle de eventos) que para verificar que la lógica pedida realmente quedó implementada como se diseñó; el piso de probabilidad es un buen ejemplo de algo que pedí, que la IA aceptó implementar, pero que al final no quedó en el código y solo lo detecté probando `portero.probabilidades()` directamente.
- Ventaja del vibecoding: permite iterar muy rápido tanto en UI como en lógica de juego, probando ideas sin escribir todo desde cero.
- Límite del vibecoding: que el código compile y las pruebas existentes pasen no garantiza que cumpla exactamente lo que se pidió; hay que validar con casos concretos (como correr `probabilidades()` con un escenario extremo) y no confiar solo en que "funciona".
- Comprendo bien el ciclo principal en `main.py`, el flujo del menú en `menu.py`, y la lógica de disparos y animación en `juego.py`. Lo que necesito reforzar es el diseño de la lógica de pesos en `portero.py` (cómo implementar correctamente un piso mínimo de probabilidad redistribuyendo el resto) y el manejo de superficies con transparencia (`pygame.SRCALPHA`) que usa `ui.py` para los paneles y el efecto de luces del estadio.

<img width="1267" height="890" alt="image" src="https://github.com/user-attachments/assets/bd77a553-29fc-4f4a-92a8-ac8da1e28cc5" />
<img width="1263" height="893" alt="image" src="https://github.com/user-attachments/assets/0f0fa642-5a4e-4252-8d08-b311a584bc8b" />


