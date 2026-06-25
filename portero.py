import random

ZONAS = ['izquierda', 'centro', 'derecha']


class Portero:
    def __init__(self, semilla=None):
        self.elecciones_jugador = {zona: 0 for zona in ZONAS}
        self.aleatorio = random.Random(semilla)

    def elegir_zona(self):
        pesos = [1.0 + 0.6 * self.elecciones_jugador[zona] for zona in ZONAS]
        return self.aleatorio.choices(ZONAS, weights=pesos, k=1)[0]

    def registrar_eleccion(self, zona):
        if zona in self.elecciones_jugador:
            self.elecciones_jugador[zona] += 1

    def probabilidades(self):
        pesos = [1.0 + 0.6 * self.elecciones_jugador[zona] for zona in ZONAS]
        total = sum(pesos)
        return {zona: peso / total for zona, peso in zip(ZONAS, pesos)}
