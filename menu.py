TEAMS = [
    {
        'name': 'Canadá',
        'code': 'CAN',
        'colors': [(255, 255, 255), (173, 0, 14)],
        'pattern': 'canada',
    },
    {
        'name': 'Brasil',
        'code': 'BRA',
        'colors': [(0, 155, 58), (255, 223, 0), (0, 39, 118)],
        'pattern': 'brazil',
    },
    {
        'name': 'México',
        'code': 'MEX',
        'colors': [(0, 104, 71), (255, 255, 255), (206, 17, 38)],
        'pattern': 'mexico',
    },
    {
        'name': 'España',
        'code': 'ESP',
        'colors': [(198, 12, 48), (252, 209, 22)],
        'pattern': 'spain',
    },
    {
        'name': 'Japón',
        'code': 'JPN',
        'colors': [(255, 255, 255), (188, 0, 45)],
        'pattern': 'japan',
    },
    {
        'name': 'Francia',
        'code': 'FRA',
        'colors': [(0, 85, 164), (255, 255, 255), (239, 65, 53)],
        'pattern': 'france',
    },
    {
        'name': 'Argentina',
        'code': 'ARG',
        'colors': [(116, 172, 223), (255, 255, 255), (255, 212, 0)],
        'pattern': 'argentina',
    },
    {
        'name': 'Marruecos',
        'code': 'MAR',
        'colors': [(206, 17, 38), (0, 94, 45)],
        'pattern': 'morocco',
    },
]

COLUMNS = 4


class Menu:
    def __init__(self):
        self.fase = 'player'
        self.player_index = 0
        self.opponent_index = 1
        self.visible = True
        self.seleccionados = {'player': None, 'opponent': None}

    def mover(self, delta):
        if self.fase == 'player':
            self.player_index = self._ajustar_indice(self.player_index + delta)
            if self.player_index == self.opponent_index:
                self.opponent_index = self._ajustar_indice(self.player_index + 1)
        else:
            self.opponent_index = self._ajustar_indice(self.opponent_index + delta)
            if self.opponent_index == self.player_index:
                self.opponent_index = self._ajustar_indice(self.opponent_index + delta)

    def confirmar(self):
        if self.fase == 'player':
            self.seleccionados['player'] = TEAMS[self.player_index]
            self.fase = 'opponent'
            if self.opponent_index == self.player_index:
                self.opponent_index = self._ajustar_indice(self.player_index + 1)
        else:
            self.seleccionados['opponent'] = TEAMS[self.opponent_index]
            self.visible = False

    def cancelar(self):
        if self.fase == 'opponent':
            self.fase = 'player'
        else:
            self.visible = False

    def equipos_confirmados(self):
        return self.seleccionados['player'], self.seleccionados['opponent']

    def equipo_actual(self):
        return TEAMS[self.player_index] if self.fase == 'player' else TEAMS[self.opponent_index]

    def equipo_seleccionado(self):
        if self.fase == 'player':
            return TEAMS[self.player_index]
        return TEAMS[self.opponent_index]

    def sincronizar_indices(self):
        if self.seleccionados['player']:
            self.player_index = self._indice_por_equipo(self.seleccionados['player'])
        if self.seleccionados['opponent']:
            self.opponent_index = self._indice_por_equipo(self.seleccionados['opponent'])
        if self.player_index == self.opponent_index:
            self.opponent_index = self._ajustar_indice(self.player_index + 1)

    def reset(self):
        self.fase = 'player'
        self.player_index = 0
        self.opponent_index = 1
        self.visible = True
        self.seleccionados = {'player': None, 'opponent': None}

    def _indice_por_equipo(self, equipo):
        for index, equipo_def in enumerate(TEAMS):
            if equipo_def['code'] == equipo.get('code'):
                return index
        return 0

    def _ajustar_indice(self, indice):
        total = len(TEAMS)
        return indice % total
