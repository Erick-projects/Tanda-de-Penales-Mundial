import pygame
from portero import ZONAS
from menu import TEAMS

COLOR_BG = (10, 20, 42)
COLOR_CESPED = (20, 100, 52)
COLOR_CESPED_STRIPE = (35, 145, 74)
COLOR_CESPED_HIGHLIGHT = (72, 190, 98)
COLOR_CESPED_SHADOW = (16, 88, 46)
COLOR_LINEAS = (245, 248, 252)
COLOR_PORTERO = (26, 90, 170)
COLOR_PORTERO_SHADOW = (10, 18, 32)
COLOR_PORTERO_TEX = (245, 245, 245)
COLOR_PELOTA = (250, 250, 250)
COLOR_SOMBRA = (12, 12, 12, 110)
COLOR_ARCO = (245, 245, 250)
COLOR_ARCO_POST = (232, 232, 240)
COLOR_GOAL_POST = (240, 240, 245)
COLOR_GOAL_SHADOW = (0, 0, 0, 70)
COLOR_RED = (210, 85, 110)
COLOR_TEXT = (245, 248, 253)
COLOR_PANEL = (14, 26, 46)
COLOR_ACCENT = (255, 190, 54)
COLOR_ACCENT_2 = (255, 135, 55)
COLOR_MENU_CARD = (18, 34, 66)
COLOR_MENU_ACTIVE = (80, 155, 255)
COLOR_MENU_BORDER = (255, 210, 80)
COLOR_BUTTON = (28, 50, 86)
COLOR_BUTTON_HIGHLIGHT = (90, 140, 245)
COLOR_GOAL_BG = (18, 42, 78)
COLOR_SPOTLIGHT = (255, 255, 255, 28)
COLOR_SHADOW_OVERLAY = (0, 0, 0, 80)
COLOR_PORTERO_ACCENT = (105, 180, 255)
COLOR_PELOTA_LINE = (55, 55, 55)
COLOR_PELOTA_SHINE = (235, 235, 240)

GOAL_RECT = pygame.Rect(260, 120, 420, 180)


class UI:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente = pygame.font.SysFont('Arial', 22)
        self.fuente_titulo = pygame.font.SysFont('Arial', 40, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont('Arial', 26)
        self.fuente_mini = pygame.font.SysFont('Arial', 18)
        self.fuente_boton = pygame.font.SysFont('Arial', 24, bold=True)

    def pintar(self, juego, menu=None):
        if menu and menu.visible:
            self._dibujar_menu(menu)
        else:
            self._dibujar_partido(juego)

    def _dibujar_partido(self, juego):
        self.pantalla.fill(COLOR_BG)
        self._dibujar_publico()
        self._dibujar_cesped()
        self._dibujar_estadio()
        self._dibujar_puntos(juego)
        self._dibujar_portero(juego.posicion_portero)
        self._dibujar_pelota(juego.posicion_pelota)
        self._dibujar_ui(juego)

    def _dibujar_publico(self):
        grada = pygame.Surface((1024, 120), pygame.SRCALPHA)
        for i in range(0, 1024, 20):
            color = (55, 75, 115, 100) if (i // 20) % 2 == 0 else (45, 65, 105, 100)
            pygame.draw.rect(grada, color, (i, 0, 20, 120))
        self.pantalla.blit(grada, (0, 0))

        overlay = pygame.Surface((1024, 120), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        self.pantalla.blit(overlay, (0, 0))

        beams = pygame.Surface((1024, 120), pygame.SRCALPHA)
        for i in range(0, 1024, 160):
            pygame.draw.polygon(beams, (255, 255, 255, 14), [(i, 0), (i + 120, 0), (i + 170, 120), (i - 50, 120)])
        self.pantalla.blit(beams, (0, 0), special_flags=pygame.BLEND_ADD)

    def _dibujar_cesped(self):
        self.pantalla.fill(COLOR_CESPED)
        for i in range(0, 1024, 64):
            color = COLOR_CESPED_STRIPE if (i // 64) % 2 == 0 else COLOR_CESPED
            pygame.draw.rect(self.pantalla, color, (i, 0, 32, 700))

        pygame.draw.rect(self.pantalla, COLOR_LINEAS, (280, 130, 380, 160), width=4, border_radius=20)
        pygame.draw.ellipse(self.pantalla, COLOR_LINEAS, (350, 180, 324, 88), width=4)

    def _dibujar_estadio(self):
        light = pygame.Surface((GOAL_RECT.width + 260, GOAL_RECT.height + 260), pygame.SRCALPHA)
        pygame.draw.circle(light, COLOR_SPOTLIGHT, (light.get_width() // 2, light.get_height() // 2), 280)
        self.pantalla.blit(light, (GOAL_RECT.x - 120, GOAL_RECT.y - 120), special_flags=pygame.BLEND_ADD)

        shadow = pygame.Surface((GOAL_RECT.width + 60, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, COLOR_GOAL_SHADOW, shadow.get_rect())
        self.pantalla.blit(shadow, (GOAL_RECT.x - 30, GOAL_RECT.y + GOAL_RECT.height - 10))

        pygame.draw.rect(self.pantalla, COLOR_GOAL_BG, GOAL_RECT, border_radius=22)
        pygame.draw.rect(self.pantalla, COLOR_GOAL_POST, (GOAL_RECT.x - 16, GOAL_RECT.y - 16, 32, GOAL_RECT.height + 32), border_radius=12)
        pygame.draw.rect(self.pantalla, COLOR_GOAL_POST, (GOAL_RECT.right - 16, GOAL_RECT.y - 16, 32, GOAL_RECT.height + 32), border_radius=12)
        pygame.draw.rect(self.pantalla, COLOR_GOAL_POST, (GOAL_RECT.x - 16, GOAL_RECT.y - 16, GOAL_RECT.width + 32, 32), border_radius=12)
        pygame.draw.line(self.pantalla, COLOR_ARCO_POST, GOAL_RECT.midtop, GOAL_RECT.midbottom, 6)

        inner = pygame.Rect(GOAL_RECT.x + 14, GOAL_RECT.y + 14, GOAL_RECT.width - 28, GOAL_RECT.height - 28)
        pygame.draw.rect(self.pantalla, (24, 46, 80), inner, border_radius=18)

        net = pygame.Surface((inner.width, inner.height), pygame.SRCALPHA)
        for i in range(0, net.get_width(), 14):
            pygame.draw.line(net, (255, 255, 255, 40), (i, 0), (i, net.get_height()), 2)
        for j in range(0, net.get_height(), 14):
            pygame.draw.line(net, (255, 255, 255, 40), (0, j), (net.get_width(), j), 2)
        for d in range(0, net.get_width(), 28):
            pygame.draw.line(net, (255, 255, 255, 25), (d, 0), (d + 20, net.get_height()), 2)
        for d in range(0, net.get_height(), 28):
            pygame.draw.line(net, (255, 255, 255, 20), (0, d), (net.get_width(), d + 20), 2)
        self.pantalla.blit(net, (inner.x, inner.y))

        pygame.draw.line(self.pantalla, COLOR_LINEAS, GOAL_RECT.midtop, GOAL_RECT.midbottom, 4)
        pygame.draw.line(self.pantalla, COLOR_LINEAS, (GOAL_RECT.x + 20, GOAL_RECT.y + 40), (GOAL_RECT.right - 20, GOAL_RECT.y + 40), 2)
        pygame.draw.line(self.pantalla, COLOR_LINEAS, (GOAL_RECT.x + 20, GOAL_RECT.bottom - 40), (GOAL_RECT.right - 20, GOAL_RECT.bottom - 40), 2)

    def _dibujar_menu(self, menu):
        self.pantalla.fill(COLOR_BG)
        fondo = pygame.Surface((1024, 700), pygame.SRCALPHA)
        for i in range(0, 700, 22):
            pygame.draw.line(fondo, (255, 255, 255, 12), (0, i), (1024, i), 1)
        self.pantalla.blit(fondo, (0, 0))

        cabecera = pygame.Surface((900, 120), pygame.SRCALPHA)
        pygame.draw.rect(cabecera, (20, 35, 70, 230), cabecera.get_rect(), border_radius=24)
        pygame.draw.rect(cabecera, (255, 255, 255, 18), cabecera.get_rect(), width=2, border_radius=24)
        self.pantalla.blit(cabecera, (62, 28))

        titulo = self.fuente_titulo.render('Mundial 2026', True, COLOR_TEXT)
        subtitulo = self.fuente_subtitulo.render('Selecciona tu equipo y el rival antes de patear', True, COLOR_TEXT)
        controles = self.fuente_mini.render('← → = mover  |  ENTER = confirmar  |  ESC = volver atrás', True, COLOR_ACCENT)
        self.pantalla.blit(titulo, (84, 42))
        self.pantalla.blit(subtitulo, (84, 90))
        self.pantalla.blit(controles, (84, 122))

        indicador = self.fuente.render('Fase: ' + ('Jugador' if menu.fase == 'player' else 'Rival'), True, COLOR_ACCENT_2)
        self.pantalla.blit(indicador, (680, 92))

        ancho = 220
        alto = 130
        margen_x = 60
        margen_y = 190
        espacio_x = 34
        espacio_y = 30

        for index, equipo in enumerate(TEAMS):
            fila = index // 4
            col = index % 4
            x = margen_x + col * (ancho + espacio_x)
            y = margen_y + fila * (alto + espacio_y)
            rect = pygame.Rect(x, y, ancho, alto)
            seleccionado = (menu.fase == 'player' and index == menu.player_index) or (menu.fase == 'opponent' and index == menu.opponent_index)
            sombra = pygame.Surface((ancho + 18, alto + 18), pygame.SRCALPHA)
            pygame.draw.rect(sombra, (0, 0, 0, 50), sombra.get_rect(), border_radius=28)
            self.pantalla.blit(sombra, (x - 9, y - 9))
            color_fondo = (26, 42, 78) if seleccionado else COLOR_MENU_CARD
            pygame.draw.rect(self.pantalla, color_fondo, rect, border_radius=22)
            if seleccionado:
                pygame.draw.rect(self.pantalla, COLOR_ACCENT, rect.inflate(12, 12), width=4, border_radius=28)
                highlight = pygame.Surface((ancho - 24, alto * 0.22), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 18))
                self.pantalla.blit(highlight, (x + 12, y + 14))
            self._dibujar_bandera(equipo, (x + 16, y + 18), (188, 68))
            nombre = self.fuente.render(equipo['name'], True, COLOR_TEXT)
            self.pantalla.blit(nombre, (x + 16, y + 108))

        self._dibujar_previsualizacion(menu)

    def _dibujar_previsualizacion(self, menu):
        x = 60
        y = 520
        panel = pygame.Surface((900, 150), pygame.SRCALPHA)
        pygame.draw.rect(panel, (18, 34, 64, 230), panel.get_rect(), border_radius=26)
        pygame.draw.rect(panel, (255, 255, 255, 18), panel.get_rect(), width=2, border_radius=26)
        self.pantalla.blit(panel, (x, y))

        texto = self.fuente.render('Equipos seleccionados', True, COLOR_ACCENT)
        self.pantalla.blit(texto, (x + 28, y + 18))

        if menu.seleccionados['player']:
            pygame.draw.rect(self.pantalla, (255, 255, 255, 18), (x + 30, y + 44, 176, 84), border_radius=18)
            self._dibujar_bandera(menu.seleccionados['player'], (x + 34, y + 50), (160, 72))
            team_text = self.fuente.render(f'Jugador: {menu.seleccionados["player"]["name"]}', True, COLOR_TEXT)
            self.pantalla.blit(team_text, (x + 28, y + 126))

        if menu.seleccionados['opponent']:
            pygame.draw.rect(self.pantalla, (255, 255, 255, 18), (x + 470, y + 44, 176, 84), border_radius=18)
            self._dibujar_bandera(menu.seleccionados['opponent'], (x + 474, y + 50), (160, 72))
            team_text = self.fuente.render(f'Rival: {menu.seleccionados["opponent"]["name"]}', True, COLOR_TEXT)
            self.pantalla.blit(team_text, (x + 468, y + 126))

        mensaje = self.fuente_mini.render('Selecciona tu equipo primero, luego el rival.', True, COLOR_TEXT)
        self.pantalla.blit(mensaje, (x + 28, y + 110))

    def _dibujar_bandera(self, equipo, esquina, tamaño):
        x, y = esquina
        ancho, alto = tamaño
        base = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(self.pantalla, (255, 255, 255), base, border_radius=18)
        pattern = equipo['pattern']

        if pattern == 'canada':
            pygame.draw.rect(self.pantalla, (206, 17, 38), (x, y, ancho * 0.22, alto), border_radius=18)
            pygame.draw.rect(self.pantalla, (206, 17, 38), (x + ancho * 0.78, y, ancho * 0.22, alto), border_radius=18)
            pygame.draw.polygon(self.pantalla, (255, 255, 255), [
                (x + ancho * 0.47, y + alto * 0.16),
                (x + ancho * 0.52, y + alto * 0.16),
                (x + ancho * 0.58, y + alto * 0.38),
                (x + ancho * 0.52, y + alto * 0.38),
                (x + ancho * 0.54, y + alto * 0.65),
                (x + ancho * 0.50, y + alto * 0.70),
                (x + ancho * 0.46, y + alto * 0.65),
                (x + ancho * 0.48, y + alto * 0.38),
                (x + ancho * 0.42, y + alto * 0.38),
            ])
        elif pattern == 'brazil':
            pygame.draw.rect(self.pantalla, (0, 155, 58), base, border_radius=18)
            rombo = [(x + ancho * 0.13, y + alto * 0.5), (x + ancho * 0.5, y + alto * 0.08), (x + ancho * 0.87, y + alto * 0.5), (x + ancho * 0.5, y + alto * 0.92)]
            pygame.draw.polygon(self.pantalla, (255, 223, 0), rombo)
            pygame.draw.circle(self.pantalla, (0, 39, 118), (int(x + ancho * 0.5), int(y + alto * 0.5)), int(alto * 0.2))
        elif pattern == 'mexico':
            ancho_fr = ancho // 3
            pygame.draw.rect(self.pantalla, (0, 104, 71), (x, y, ancho_fr, alto), border_radius=18)
            pygame.draw.rect(self.pantalla, (255, 255, 255), (x + ancho_fr, y, ancho_fr, alto))
            pygame.draw.rect(self.pantalla, (206, 17, 38), (x + ancho_fr * 2, y, ancho_fr, alto), border_radius=18)
            pygame.draw.circle(self.pantalla, (0, 104, 71), (int(x + ancho * 0.5), int(y + alto * 0.52)), int(alto * 0.12))
            pygame.draw.circle(self.pantalla, (255, 255, 255), (int(x + ancho * 0.5), int(y + alto * 0.52)), int(alto * 0.07))
        elif pattern == 'spain':
            pygame.draw.rect(self.pantalla, (198, 12, 48), (x, y, ancho, alto * 0.32), border_radius=18)
            pygame.draw.rect(self.pantalla, (252, 209, 22), (x, y + alto * 0.32, ancho, alto * 0.36))
            pygame.draw.rect(self.pantalla, (198, 12, 48), (x, y + alto * 0.68, ancho, alto * 0.32), border_radius=18)
            pygame.draw.rect(self.pantalla, (255, 255, 255), (x + ancho * 0.42, y + alto * 0.35, ancho * 0.16, alto * 0.30))
        elif pattern == 'japan':
            pygame.draw.rect(self.pantalla, (255, 255, 255), base, border_radius=18)
            pygame.draw.circle(self.pantalla, (188, 0, 45), (int(x + ancho * 0.5), int(y + alto * 0.5)), int(alto * 0.22))
        elif pattern == 'france':
            ancho_fr = ancho // 3
            pygame.draw.rect(self.pantalla, (0, 85, 164), (x, y, ancho_fr, alto), border_radius=18)
            pygame.draw.rect(self.pantalla, (255, 255, 255), (x + ancho_fr, y, ancho_fr, alto))
            pygame.draw.rect(self.pantalla, (239, 65, 53), (x + ancho_fr * 2, y, ancho_fr, alto), border_radius=18)
        elif pattern == 'argentina':
            alto_fr = alto // 3
            pygame.draw.rect(self.pantalla, (116, 172, 223), (x, y, ancho, alto_fr), border_radius=18)
            pygame.draw.rect(self.pantalla, (255, 255, 255), (x, y + alto_fr, ancho, alto_fr))
            pygame.draw.rect(self.pantalla, (116, 172, 223), (x, y + alto_fr * 2, ancho, alto_fr), border_radius=18)
            pygame.draw.circle(self.pantalla, (255, 212, 0), (int(x + ancho * 0.5), int(y + alto * 0.5)), int(alto * 0.12))
            pygame.draw.circle(self.pantalla, (255, 255, 255), (int(x + ancho * 0.5), int(y + alto * 0.5)), int(alto * 0.05))
        elif pattern == 'morocco':
            pygame.draw.rect(self.pantalla, (206, 17, 38), base, border_radius=18)
            puntos = [
                (x + ancho * 0.5, y + alto * 0.18),
                (x + ancho * 0.62, y + alto * 0.55),
                (x + ancho * 0.05, y + alto * 0.38),
                (x + ancho * 0.95, y + alto * 0.38),
                (x + ancho * 0.38, y + alto * 0.55),
            ]
            pygame.draw.polygon(self.pantalla, (0, 94, 45), puntos)
            pygame.draw.polygon(self.pantalla, (255, 255, 255), [
                (x + ancho * 0.5, y + alto * 0.24),
                (x + ancho * 0.58, y + alto * 0.45),
                (x + ancho * 0.24, y + alto * 0.40),
                (x + ancho * 0.75, y + alto * 0.40),
                (x + ancho * 0.42, y + alto * 0.50),
            ])
        else:
            pygame.draw.rect(self.pantalla, equipo['colors'][0], base, border_radius=18)

    def _dibujar_pelota(self, posicion):
        sombra_rect = pygame.Rect(0, 0, 86, 24)
        sombra_rect.center = (posicion[0] + 12, posicion[1] + 34)
        sombra_surf = pygame.Surface(sombra_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, COLOR_SOMBRA, sombra_surf.get_rect())
        self.pantalla.blit(sombra_surf, sombra_rect.topleft)

        x = int(posicion[0])
        y = int(posicion[1])
        pygame.draw.circle(self.pantalla, COLOR_PELOTA, (x, y), 22)
        pygame.draw.circle(self.pantalla, COLOR_PELOTA_SHINE, (x - 7, y - 7), 8)
        pygame.draw.circle(self.pantalla, (225, 225, 225), (x + 9, y - 3), 5)

        pentagon = [(x, y - 12), (x + 10, y - 4), (x + 6, y + 9), (x - 6, y + 9), (x - 10, y - 4)]
        pygame.draw.polygon(self.pantalla, COLOR_PELOTA_LINE, pentagon)
        pygame.draw.polygon(self.pantalla, COLOR_PELOTA, [(x, y - 10), (x + 8, y - 3), (x + 5, y + 7), (x - 5, y + 7), (x - 8, y - 3)])

        blocks = [
            [(x - 24, y - 2), (x - 16, y - 10), (x - 6, y - 8), (x - 8, y - 1)],
            [(x + 24, y - 2), (x + 16, y - 10), (x + 6, y - 8), (x + 8, y - 1)],
            [(x, y + 18), (x + 8, y + 10), (x + 2, y + 2), (x - 2, y + 2), (x - 8, y + 10)],
        ]
        for block in blocks:
            pygame.draw.polygon(self.pantalla, COLOR_PELOTA_LINE, block)
            pygame.draw.polygon(self.pantalla, COLOR_PELOTA, [(px + 1, py + 1) for px, py in block])

        shine = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(shine, (255, 255, 255, 140), (12, 12), 8)
        self.pantalla.blit(shine, (x - 18, y - 18))

    def _dibujar_portero(self, posicion):
        x, y = int(posicion[0]), int(posicion[1])
        pygame.draw.ellipse(self.pantalla, (8, 16, 34, 140), (x - 36, y + 20, 72, 24))

        torso = pygame.Surface((64, 86), pygame.SRCALPHA)
        pygame.draw.ellipse(torso, COLOR_PORTERO, (4, 20, 56, 58))
        pygame.draw.rect(torso, COLOR_PORTERO, (18, 0, 28, 40), border_radius=18)
        pygame.draw.circle(torso, COLOR_PORTERO, (32, 12), 16)
        pygame.draw.rect(torso, COLOR_ACCENT_2, (12, 34, 40, 14), border_radius=8)
        pygame.draw.polygon(torso, (40, 120, 215), [(18, 20), (18, 40), (10, 56), (8, 54)])
        pygame.draw.polygon(torso, (40, 120, 215), [(46, 20), (46, 40), (54, 56), (56, 54)])
        self.pantalla.blit(torso, (x - 32, y - 44))

        brazo_izq = [(x - 26, y - 6), (x - 68, y + 8), (x - 58, y + 18), (x - 24, y + 2)]
        brazo_der = [(x + 26, y - 6), (x + 68, y + 8), (x + 58, y + 18), (x + 24, y + 2)]
        pygame.draw.polygon(self.pantalla, COLOR_PORTERO, brazo_izq)
        pygame.draw.polygon(self.pantalla, COLOR_PORTERO, brazo_der)

        pygame.draw.circle(self.pantalla, (245, 245, 245), (x - 68, y + 18), 10)
        pygame.draw.circle(self.pantalla, (245, 245, 245), (x + 68, y + 18), 10)

        pygame.draw.circle(self.pantalla, COLOR_PORTERO_TEX, (x - 6, y - 38), 4)
        pygame.draw.circle(self.pantalla, COLOR_PORTERO_TEX, (x + 6, y - 38), 4)
        pygame.draw.polygon(self.pantalla, COLOR_PORTERO_TEX, [(x - 12, y - 26), (x + 12, y - 26), (x + 8, y - 18), (x - 8, y - 18)])

        brillo = pygame.Surface((64, 86), pygame.SRCALPHA)
        pygame.draw.rect(brillo, (255, 255, 255, 18), (12, 34, 40, 12), border_radius=6)
        pygame.draw.ellipse(brillo, (255, 255, 255, 12), (18, 6, 28, 16))
        self.pantalla.blit(brillo, (x - 32, y - 44))

        pygame.draw.polygon(self.pantalla, (24, 96, 185), [(x - 32, y - 8), (x - 56, y + 8), (x - 52, y + 12), (x - 30, y)])
        pygame.draw.polygon(self.pantalla, (24, 96, 185), [(x + 32, y - 8), (x + 56, y + 8), (x + 52, y + 12), (x + 30, y)])

        pygame.draw.line(self.pantalla, COLOR_PORTERO_TEX, (x - 4, y - 24), (x + 4, y - 24), 2)
        pygame.draw.line(self.pantalla, COLOR_PORTERO_TEX, (x - 2, y - 18), (x + 2, y - 18), 2)

    def _dibujar_puntos(self, juego):
        score_panel = pygame.Surface((260, 170), pygame.SRCALPHA)
        pygame.draw.rect(score_panel, (16, 24, 48, 240), score_panel.get_rect(), border_radius=26)
        pygame.draw.rect(score_panel, (255, 255, 255, 18), score_panel.get_rect(), width=2, border_radius=26)
        pygame.draw.rect(score_panel, COLOR_ACCENT, (0, 0, 260, 8), border_radius=4)
        self.pantalla.blit(score_panel, (30, 24))

        titulo = self.fuente_subtitulo.render('Marcador', True, COLOR_TEXT)
        self.pantalla.blit(titulo, (40, 38))

        marcador = self.fuente_boton.render(f'{juego.goles} - {max(0, juego.tiros - juego.goles)}', True, COLOR_ACCENT)
        self.pantalla.blit(marcador, (40, 82))

        self.pantalla.blit(self.fuente.render(f'Tiros: {juego.tiros}/5', True, COLOR_ACCENT), (40, 132))
        self.pantalla.blit(self.fuente.render(f'Goles: {juego.goles}', True, COLOR_ACCENT), (156, 132))

        teams_panel = pygame.Surface((260, 128), pygame.SRCALPHA)
        pygame.draw.rect(teams_panel, (16, 24, 48, 220), teams_panel.get_rect(), border_radius=26)
        pygame.draw.rect(teams_panel, (255, 255, 255, 18), teams_panel.get_rect(), width=2, border_radius=26)
        pygame.draw.rect(teams_panel, COLOR_ACCENT_2, (0, 0, 260, 6), border_radius=4)
        self.pantalla.blit(teams_panel, (30, 206))

        self.pantalla.blit(self.fuente_subtitulo.render('Jugador', True, COLOR_TEXT), (40, 216))
        self.pantalla.blit(self.fuente_subtitulo.render('Rival', True, COLOR_TEXT), (142, 216))

        if juego.player_team and juego.opponent_team:
            self._dibujar_bandera(juego.player_team, (40, 248), (64, 32))
            self._dibujar_bandera(juego.opponent_team, (142, 248), (64, 32))
            self.pantalla.blit(self.fuente_mini.render(juego.player_team['name'], True, COLOR_TEXT), (40, 286))
            self.pantalla.blit(self.fuente_mini.render(juego.opponent_team['name'], True, COLOR_TEXT), (142, 286))
        else:
            self.pantalla.blit(self.fuente_mini.render('Jugador: ---', True, COLOR_TEXT), (40, 286))
            self.pantalla.blit(self.fuente_mini.render('Rival: ---', True, COLOR_TEXT), (142, 286))

    def _dibujar_ui(self, juego):
        controls_panel = pygame.Surface((300, 196), pygame.SRCALPHA)
        pygame.draw.rect(controls_panel, (16, 26, 46, 240), controls_panel.get_rect(), border_radius=26)
        pygame.draw.rect(controls_panel, (255, 255, 255, 16), controls_panel.get_rect(), width=2, border_radius=26)
        pygame.draw.rect(controls_panel, COLOR_ACCENT, (0, 0, 300, 8), border_radius=4)
        self.pantalla.blit(controls_panel, (694, 24))

        subtitle = self.fuente_subtitulo.render('Controles', True, COLOR_TEXT)
        self.pantalla.blit(subtitle, (710, 40))

        instructions_box = pygame.Surface((276, 132), pygame.SRCALPHA)
        pygame.draw.rect(instructions_box, (12, 22, 36, 220), instructions_box.get_rect(), border_radius=22)
        pygame.draw.rect(instructions_box, (255, 255, 255, 16), instructions_box.get_rect(), width=2, border_radius=22)
        self.pantalla.blit(instructions_box, (708, 72))

        instrucciones = [
            '← / →  cambiar zona',
            'ESPACIO  disparar',
            'ESC  regresar menú',
            'R  reiniciar al terminar',
        ]
        for index, linea in enumerate(instrucciones, start=1):
            texto = self.fuente_mini.render(linea, True, COLOR_TEXT)
            self.pantalla.blit(texto, (722, 90 + (index - 1) * 28))

        zone_panel = pygame.Surface((300, 120), pygame.SRCALPHA)
        pygame.draw.rect(zone_panel, (12, 22, 36, 220), zone_panel.get_rect(), border_radius=24)
        pygame.draw.rect(zone_panel, (255, 255, 255, 18), zone_panel.get_rect(), width=2, border_radius=24)
        self.pantalla.blit(zone_panel, (694, 240))

        hint = self.fuente_subtitulo.render('Zona activa', True, COLOR_TEXT)
        self.pantalla.blit(hint, (710, 252))
        info_zone = self.fuente_mini.render('Selecciona tu tiro', True, COLOR_ACCENT)
        self.pantalla.blit(info_zone, (710, 282))

        for i, zona in enumerate(ZONAS, start=1):
            cx = 726 + (i - 1) * 88
            cy = 318
            color = COLOR_ACCENT if juego.seleccion_actual == i else COLOR_BUTTON_HIGHLIGHT
            pygame.draw.circle(self.pantalla, (16, 26, 46), (cx, cy), 20)
            pygame.draw.circle(self.pantalla, color, (cx, cy), 12)
            etiqueta = self.fuente_mini.render(zona[0].upper(), True, COLOR_TEXT)
            self.pantalla.blit(etiqueta, (cx - etiqueta.get_width() // 2, cy - etiqueta.get_height() // 2))

        if juego.terminado:
            resultado = 'GANASTE' if juego.goles >= 3 else 'PERDISTE'
            mensaje = f'Fin de la tanda: {resultado}'
            texto_final = self.fuente_subtitulo.render(mensaje, True, COLOR_ACCENT)
            self.pantalla.blit(texto_final, (220, 620 - 50))
            subtitulo = self.fuente.render('Presiona R para otra o ESC para menú', True, COLOR_TEXT)
            self.pantalla.blit(subtitulo, (220, 660 - 50))
