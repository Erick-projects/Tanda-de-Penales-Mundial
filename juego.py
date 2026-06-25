from animacion import Animacion
from portero import ZONAS

ZONA_POSICIONES = {
    'izquierda': (340, 250),
    'centro': (500, 230),
    'derecha': (660, 250),
}
PORTERO_POSICIONES = {
    'izquierda': (340, 265),
    'centro': (500, 280),
    'derecha': (660, 265),
}
PELOTA_INICIAL = (500, 560)
PORTERO_INICIAL = (500, 320)


class Juego:
    def __init__(self, portero):
        self.portero = portero
        self.player_team = None
        self.opponent_team = None
        self.reiniciar()

    def reiniciar(self):
        self.tiros = 0
        self.goles = 0
        self.terminado = False
        self.seleccion_actual = 1
        self.resultado_ultimo = None
        self.animacion_pelota = None
        self.animacion_portero = None
        self.animacion_activa = False

    def mover_seleccion(self, delta):
        if self.terminado or self.animacion_activa:
            return
        self.seleccion_actual = max(1, min(len(ZONAS), self.seleccion_actual + delta))

    def iniciar_disparo(self):
        if self.terminado or self.animacion_activa:
            return None

        zona_jugador = ZONAS[self.seleccion_actual - 1]
        zona_portero = self.portero.elegir_zona()
        atajado = zona_jugador == zona_portero
        if not atajado:
            self.goles += 1

        self.portero.registrar_eleccion(zona_jugador)
        self.tiros += 1
        self.terminado = self.tiros >= 5
        self.resultado_ultimo = {
            'zona': zona_jugador,
            'atajado': atajado,
            'zona_portero': zona_portero,
        }
        self.animacion_pelota = Animacion(PELOTA_INICIAL, ZONA_POSICIONES[zona_jugador], 0.8)
        self.animacion_portero = Animacion(PORTERO_INICIAL, PORTERO_POSICIONES[zona_portero], 0.8)
        self.animacion_activa = True
        return self.resultado_ultimo

    def actualizar(self, dt):
        if not self.animacion_activa:
            return
        self.animacion_pelota.actualizar(dt)
        self.animacion_portero.actualizar(dt)
        if self.animacion_pelota.terminado and self.animacion_portero.terminado:
            self.animacion_activa = False

    @property
    def posicion_pelota(self):
        if self.animacion_pelota:
            return self.animacion_pelota.valor
        return PELOTA_INICIAL

    @property
    def posicion_portero(self):
        if self.animacion_portero:
            return self.animacion_portero.valor
        return PORTERO_INICIAL
