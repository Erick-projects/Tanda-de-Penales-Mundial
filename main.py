import os
import math
import random
import array
import pygame
from juego import Juego
from portero import Portero
from ui import UI
from menu import Menu

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700


def generar_tono(frecuencia=440, duracion=0.22, volumen=0.5, sample_rate=44100):
    longitud = int(sample_rate * duracion)
    onda = array.array('h')
    max_amp = int(32767 * volumen)
    for n in range(longitud):
        t = n / sample_rate
        valor = int(max_amp * math.sin(2 * math.pi * frecuencia * t))
        onda.append(valor)
    return pygame.mixer.Sound(buffer=onda)


def cargar_sonidos():
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        return {
            'silbato': generar_tono(920, 0.18, 0.5),
            'gol': generar_tono(660, 0.28, 0.55),
            'atajada': generar_tono(320, 0.3, 0.5),
            'menu': generar_tono(520, 0.14, 0.35),
        }
    except pygame.error:
        return {'silbato': None, 'gol': None, 'atajada': None, 'menu': None}


def reproducir_sonido(sonido):
    if sonido:
        try:
            sonido.play()
        except pygame.error:
            pass


def main():
    os.environ.setdefault('SDL_VIDEO_CENTERED', '1')
    pygame.init()
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tanda de Penales — Mundial 2026')
    reloj = pygame.time.Clock()

    ui = UI(pantalla)
    menu = Menu()
    portero = Portero(semilla=42)
    juego = Juego(portero)
    sonidos = cargar_sonidos()
    reproducir_sonido(sonidos['silbato'])

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.KEYDOWN:
                if menu.visible:
                    if evento.key == pygame.K_LEFT:
                        menu.mover(-1)
                        reproducir_sonido(sonidos['menu'])
                    elif evento.key == pygame.K_RIGHT:
                        menu.mover(1)
                        reproducir_sonido(sonidos['menu'])
                    elif evento.key == pygame.K_RETURN:
                        menu.confirmar()
                        reproducir_sonido(sonidos['menu'])
                        if not menu.visible:
                            jugador, rival = menu.equipos_confirmados()
                            if jugador and rival:
                                juego.player_team = jugador
                                juego.opponent_team = rival
                    elif evento.key == pygame.K_ESCAPE:
                        menu.cancelar()
                        reproducir_sonido(sonidos['menu'])
                else:
                    if evento.key == pygame.K_LEFT:
                        juego.mover_seleccion(-1)
                    elif evento.key == pygame.K_RIGHT:
                        juego.mover_seleccion(1)
                    elif evento.key == pygame.K_SPACE and not juego.terminado and not juego.animacion_activa:
                        resultado = juego.iniciar_disparo()
                        if resultado:
                            reproducir_sonido(sonidos['atajada'] if resultado['atajado'] else sonidos['gol'])
                    elif evento.key == pygame.K_ESCAPE:
                        menu.visible = True
                        menu.fase = 'player'
                        menu.seleccionados['player'] = juego.player_team
                        menu.seleccionados['opponent'] = juego.opponent_team
                        menu.sincronizar_indices()
                        juego.reiniciar()
                        reproducir_sonido(sonidos['menu'])
                    elif evento.key == pygame.K_r and juego.terminado:
                        juego.reiniciar()
                        reproducir_sonido(sonidos['silbato'])

        if not menu.visible:
            juego.actualizar(dt)

        ui.pintar(juego, menu)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
