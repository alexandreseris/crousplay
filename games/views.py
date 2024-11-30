from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypeVar

from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, QueryDict
from django.template import loader

from games import models


def search_page(request: HttpRequest) -> HttpResponse:
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


T = TypeVar("T")


def extract_param_from_query(query: QueryDict, propname: str, type: type[T]) -> T | None:
    lookup: str | None = query.getlist(propname, [None])[0]
    if lookup:
        return type(lookup)  # type: ignore
    return None


@dataclass
class SearchParam:
    players: int | None
    duration: int | None
    level: str | None
    type: str | None
    ambiances: list[str] | None
    genres: list[str] | None

    @classmethod
    def from_querydict(cls, query: QueryDict):
        try:
            obj = cls(
                players=extract_param_from_query(query, "players", int),
                duration=extract_param_from_query(query, "duration", int),
                level=extract_param_from_query(query, "level", str),
                type=extract_param_from_query(query, "type", str),
                ambiances=query.getlist("ambiances", None),
                genres=query.getlist("genres", None),
            )
            return obj
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


def search_result(request: HttpRequest) -> HttpResponse:
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


def list_all(request: HttpRequest) -> HttpResponse:
    games = models.Game.all()
    games_data = GameProperties.from_games(games)
    template = loader.get_template("games/search.html")
    return HttpResponse(
        template.render(
            {"games": games_data},
            request,
        )
    )


def about(request: HttpRequest) -> HttpResponse:
    template = loader.get_template("games/about.html")
    return HttpResponse(template.render({}, request))
