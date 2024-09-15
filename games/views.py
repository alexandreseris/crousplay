from collections.abc import Iterable
from dataclasses import dataclass

from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, QueryDict
from django.template import loader

from games import models


def search_page(request: HttpRequest):
    template = loader.get_template("games/index.html")
    return HttpResponse(
        template.render(
            {
                "levels": models.Level.list(),
                "types": models.Type.list(),
                "ambiances": models.Ambiance.list(),
                "genres": models.Genre.list(),
            },
            request,
        )
    )


@dataclass
class SearchParam:
    players: int
    duration: int
    level: str
    type: str
    ambiances: list[str]
    genres: list[str]

    @classmethod
    def from_querydict(cls, query: QueryDict):
        try:
            return cls(
                players=int(query.getlist("players")[0]),
                duration=int(query.getlist("duration")[0]),
                level=query.getlist("level")[0],
                type=query.getlist("type")[0],
                ambiances=query.getlist("ambiances"),
                genres=query.getlist("genres"),
            )
        except Exception:
            raise SuspiciousOperation("wrong parameters")


class GameProperty:
    def __init__(self, name: str, has: bool) -> None:
        self.name = name
        self.has = has

    def __str__(self) -> str:
        return f"{self.name}={self.has}"


class GameProperties:
    def __init__(self, levels: list[GameProperty], types: list[GameProperty]) -> None:
        self.levels = levels
        self.types = types

    def __str__(self) -> str:
        levels = ", ".join([str(x) for x in self.levels])
        types = ", ".join([str(x) for x in self.types])
        return f"levels:{levels}; types:{types}"

    @classmethod
    def from_games(cls, games: Iterable[models.Game]):
        levels = [i.name for i in models.Level.list()]
        types = [i.name for i in models.Type.list()]
        for game in games:
            game_levels = [x.name for x in game.levels.all()]
            game_types = [x.name for x in game.types.all()]
            props = cls(
                levels=[GameProperty(x, x in game_levels) for x in levels],
                types=[GameProperty(x, x in game_types) for x in types],
            )
            yield game, props


def search_result(request: HttpRequest):
    params = SearchParam.from_querydict(request.GET)
    games = models.Game.search(
        players=params.players,
        duration=params.duration,
        level=params.level,
        type=params.type,
        ambiances=params.ambiances,
        genres=params.genres,
    )
    games_data = GameProperties.from_games(games)
    template = loader.get_template("games/search.html")
    return HttpResponse(
        template.render(
            {"games": games_data},
            request,
        )
    )
