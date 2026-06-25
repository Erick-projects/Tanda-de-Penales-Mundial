import os
import unittest

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import pygame
from juego import Juego
from portero import Portero, ZONAS
from menu import Menu


class TestTandaPenales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_juego_termina_despues_de_cinco_tiros(self):
        portero = Portero(semilla=0)
        juego = Juego(portero)

        for i in range(5):
            self.assertFalse(juego.terminado)
            self.assertFalse(juego.animacion_activa)
            juego.iniciar_disparo()
            self.assertTrue(juego.animacion_activa)
            while juego.animacion_activa:
                juego.actualizar(0.1)

        self.assertEqual(juego.tiros, 5)
        self.assertTrue(juego.terminado)
        self.assertIn(juego.resultado_ultimo['zona'], ZONAS)
        self.assertIn(juego.resultado_ultimo['zona_portero'], ZONAS)

    def test_portero_adaptativo_aumenta_probabilidad_para_zona_elegida(self):
        portero = Portero(semilla=123)

        for zona in ['derecha', 'derecha', 'derecha', 'izquierda']:
            portero.registrar_eleccion(zona)

        probabilidades = portero.probabilidades()
        self.assertGreater(probabilidades['derecha'], probabilidades['centro'])
        self.assertGreater(probabilidades['derecha'], probabilidades['izquierda'])

    def test_portero_elige_zona_con_pesos_adaptativos(self):
        portero = Portero(semilla=10)
        portero.registrar_eleccion('centro')
        portero.registrar_eleccion('centro')
        portero.registrar_eleccion('izquierda')

        conteo = {'izquierda': 0, 'centro': 0, 'derecha': 0}
        for _ in range(200):
            zona = portero.elegir_zona()
            conteo[zona] += 1

        self.assertGreater(conteo['centro'], conteo['izquierda'])
        self.assertGreater(conteo['centro'], conteo['derecha'])

    def test_menu_selecciona_dos_equipos_distintos(self):
        menu = Menu()
        self.assertEqual(menu.fase, 'player')
        menu.mover(1)
        menu.confirmar()
        self.assertEqual(menu.fase, 'opponent')
        menu.mover(1)
        menu.confirmar()
        self.assertFalse(menu.visible)

        jugador, rival = menu.equipos_confirmados()
        self.assertIsNotNone(jugador)
        self.assertIsNotNone(rival)
        self.assertNotEqual(jugador['code'], rival['code'])


if __name__ == '__main__':
    unittest.main()
