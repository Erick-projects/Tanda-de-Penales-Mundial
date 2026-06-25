import math


def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2


def interpolar(a, b, t):
    return a + (b - a) * t


def interpolar_posicion(inicio, fin, progreso, easing=ease_in_out_cubic):
    progreso = max(0.0, min(1.0, progreso))
    valor = easing(progreso)
    return (
        interpolar(inicio[0], fin[0], valor),
        interpolar(inicio[1], fin[1], valor),
    )


class Animacion:
    def __init__(self, inicio, fin, duracion, easing=ease_in_out_cubic):
        self.inicio = inicio
        self.fin = fin
        self.duracion = max(duracion, 0.001)
        self.easing = easing
        self.tiempo = 0.0

    def actualizar(self, dt):
        self.tiempo = min(self.duracion, self.tiempo + dt)

    @property
    def terminado(self):
        return self.tiempo >= self.duracion

    @property
    def progreso(self):
        return self.tiempo / self.duracion

    @property
    def valor(self):
        return interpolar_posicion(self.inicio, self.fin, self.progreso, self.easing)
