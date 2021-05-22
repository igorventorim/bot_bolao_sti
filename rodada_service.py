import requests
import json
import partida_api
import datetime
import dateutil.parser
import ipdb


class RodadaService():

    def __init__(self, numero):
        self.r = requests.get(
            'https://api.globoesporte.globo.com/tabela/d1a37fa4-e948-43a6-ba53-ab24ab3a45b1/fase/fase-unica-campeonato-brasileiro-2021/rodada/{}/jogos/'.format(numero))
        self.info_rodada = partida_api.partida_from_dict(self.r.json())

    def getJogosRodadaBrasileirao(self):
        # ipdb.set_trace()
        result = ""
        for partida in self.info_rodada:
            result += "{} - {}{} x {}{}\n".format(self.__getDataFormatada(partida.data_realizacao),
                                                  partida.equipes.mandante.nome_popular,
                                                  partida.placar_oficial_mandante is not None if partida.placar_oficial_mandante else "",
                                                  partida.placar_oficial_visitante is not None if partida.placar_oficial_visitante else "",
                                                  partida.equipes.visitante.nome_popular)

        return result

    def __getDataFormatada(self, dataIso):
        try:
            date = dateutil.parser.parse(dataIso)
            return date.strftime("%d/%m/%Y (%H:%M)")
        except:
            return "Não definido"
