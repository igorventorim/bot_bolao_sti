# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from typing import Any, List, Optional, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Time:
    id: int
    nome_popular: str
    sigla: str
    escudo: str

    def __init__(self, id: int, nome_popular: str, sigla: str, escudo: str) -> None:
        self.id = id
        self.nome_popular = nome_popular
        self.sigla = sigla
        self.escudo = escudo

    @staticmethod
    def from_dict(obj: Any) -> 'Time':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        nome_popular = from_str(obj.get("nome_popular"))
        sigla = from_str(obj.get("sigla"))
        escudo = from_str(obj.get("escudo"))
        return Time(id, nome_popular, sigla, escudo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["nome_popular"] = from_str(self.nome_popular)
        result["sigla"] = from_str(self.sigla)
        result["escudo"] = from_str(self.escudo)
        return result


class Equipes:
    mandante: Time
    visitante: Time

    def __init__(self, mandante: Time, visitante: Time) -> None:
        self.mandante = mandante
        self.visitante = visitante

    @staticmethod
    def from_dict(obj: Any) -> 'Equipes':
        assert isinstance(obj, dict)
        mandante = Time.from_dict(obj.get("mandante"))
        visitante = Time.from_dict(obj.get("visitante"))
        return Equipes(mandante, visitante)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mandante"] = to_class(Time, self.mandante)
        result["visitante"] = to_class(Time, self.visitante)
        return result


class Sede:
    nome_popular: str

    def __init__(self, nome_popular: str) -> None:
        self.nome_popular = nome_popular

    @staticmethod
    def from_dict(obj: Any) -> 'Sede':
        assert isinstance(obj, dict)
        nome_popular = from_str(obj.get("nome_popular"))
        return Sede(nome_popular)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nome_popular"] = from_str(self.nome_popular)
        return result


class Partida:
    id: int
    data_realizacao: Optional[str]
    hora_realizacao: Optional[str]
    placar_oficial_visitante: None
    placar_oficial_mandante: None
    placar_penaltis_visitante: None
    placar_penaltis_mandante: None
    equipes: Equipes
    sede: Sede
    transmissao: None

    def __init__(self, id: int, data_realizacao: str, hora_realizacao: str, placar_oficial_visitante: None, placar_oficial_mandante: None, placar_penaltis_visitante: None, placar_penaltis_mandante: None, equipes: Equipes, sede: Sede, transmissao: None) -> None:
        self.id = id
        self.data_realizacao = data_realizacao
        self.hora_realizacao = hora_realizacao
        self.placar_oficial_visitante = placar_oficial_visitante
        self.placar_oficial_mandante = placar_oficial_mandante
        self.placar_penaltis_visitante = placar_penaltis_visitante
        self.placar_penaltis_mandante = placar_penaltis_mandante
        self.equipes = equipes
        self.sede = sede
        self.transmissao = transmissao

    @staticmethod
    def from_dict(obj: Any) -> 'Partida':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        data_realizacao = from_union(
            [from_none, from_str], obj.get("data_realizacao"))
        hora_realizacao = from_union(
            [from_none, from_str], obj.get("hora_realizacao"))
        placar_oficial_visitante = from_none(
            obj.get("placar_oficial_visitante"))
        placar_oficial_mandante = from_none(obj.get("placar_oficial_mandante"))
        placar_penaltis_visitante = from_none(
            obj.get("placar_penaltis_visitante"))
        placar_penaltis_mandante = from_none(
            obj.get("placar_penaltis_mandante"))
        equipes = Equipes.from_dict(obj.get("equipes"))
        sede = Sede.from_dict(obj.get("sede"))
        transmissao = from_none(obj.get("transmissao"))
        return Partida(id, data_realizacao, hora_realizacao, placar_oficial_visitante, placar_oficial_mandante, placar_penaltis_visitante, placar_penaltis_mandante, equipes, sede, transmissao)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["data_realizacao"] = from_union(
            [from_none, from_str], self.data_realizacao)
        result["hora_realizacao"] = from_union(
            [from_none, from_str], self.hora_realizacao)
        result["placar_oficial_visitante"] = from_none(
            self.placar_oficial_visitante)
        result["placar_oficial_mandante"] = from_none(
            self.placar_oficial_mandante)
        result["placar_penaltis_visitante"] = from_none(
            self.placar_penaltis_visitante)
        result["placar_penaltis_mandante"] = from_none(
            self.placar_penaltis_mandante)
        result["equipes"] = to_class(Equipes, self.equipes)
        result["sede"] = to_class(Sede, self.sede)
        result["transmissao"] = from_none(self.transmissao)
        return result


def partida_from_dict(s: Any) -> List[Partida]:
    return from_list(Partida.from_dict, s)


def partida_to_dict(x: List[Partida]) -> Any:
    return from_list(lambda x: to_class(Partida, x), x)
