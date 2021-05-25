import palpite_rodada
import partida_api


class Calculador:

    def __init__(self):
        pass

    def getPontuacaoPartida(partida: Partida, palpite: Palpite):

        pontuacao = 0
        placar_mandante = partida.placar_oficial_mandante
        placar_visitante = partida.placar_oficial_visitante
        palpite_placar_mandante = palpite.placar_time_mandante
        palpite_placar_visitante = palpite.placar_time_visitante

        if placar_mandante is not None and placar_visitante is not None:

            if placar_mandante == palpite_placar_mandante and placar_visitante == palpite_placar_visitante:
                pontuacao += 2

            if (placar_mandante + placar_visitante) == (palpite_placar_mandante + palpite_placar_visitante):
                pontuacao += 1

            if (placar_mandante > placar_visitante and palpite_placar_mandante > palpite_placar_visitante) or
            (placar_mandante == placar_visitante and palpite_placar_mandante == palpite_placar_visitante) or
            (placar_mandante < partida.placar_visitante and palpite_placar_mandante < palpite_placar_visitante):
                pontuacao += 3

        return pontuacao
