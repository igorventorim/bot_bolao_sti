class Palpite:
    time_mandante: str
    placar_time_mandante: int
    time_visitante: str
    placar_time_visitante: int

    def __init__(self, time_mandante: str, placar_time_mandante: int, time_visitante: str, placar_time_visitante: str):
        self.time_mandante = time_mandante
        self.placar_time_mandante = placar_time_mandante
        self.time_visitante = time_visitante
        self.placar_time_visitante = placar_time_visitante


class PalpiteRodada:

    participante: str
    palpites: List[Palpite]

    def __init__():
        pass
