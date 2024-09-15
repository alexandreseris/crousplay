from django.core.exceptions import ValidationError
from django.db import models


def meta(friendly_name: str):
    class Meta:
        verbose_name = friendly_name

    return Meta


class Level(models.Model):
    Meta = meta("Niveau")
    name = models.CharField(verbose_name="libellé", max_length=255, null=False, unique=True)
    order = models.IntegerField(verbose_name="ordre", null=False, unique=True)

    @classmethod
    def init(cls, name: str, order: int):
        return cls(name=name, order=order)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("order").all()


class Type(models.Model):
    Meta = meta("Type")
    name = models.CharField(verbose_name="libellé", max_length=255, null=False, unique=True)
    order = models.IntegerField(verbose_name="ordre", null=False, unique=True)

    @classmethod
    def init(cls, name: str, order: int):
        return cls(name=name, order=order)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("order").all()


class Ambiance(models.Model):
    Meta = meta("Ambiance recherchée")
    name = models.CharField(verbose_name="libellé", max_length=255, null=False, unique=True)

    @classmethod
    def init(cls, name: str):
        return cls(name=name)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("name").all()


class Genre(models.Model):
    Meta = meta("Genre")
    name = models.CharField(verbose_name="libellé", max_length=255, null=False, unique=True)
    notes = models.TextField(verbose_name="notes", max_length=2048, null=False)

    @classmethod
    def init(cls, name: str, notes: str):
        return cls(name=name, notes=notes)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("name").all()


class Editor(models.Model):
    Meta = meta("Editeur")
    name = models.CharField(verbose_name="nom", max_length=255, null=False, unique=True)

    @classmethod
    def init(cls, name: str):
        return cls(name=name)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("name").all()


class Tag(models.Model):
    Meta = meta("Tag")
    name = models.CharField(verbose_name="nom", max_length=255, null=False, unique=True)

    @classmethod
    def init(cls, name: str):
        return cls(name=name)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def list(cls):
        return cls.objects.order_by("name").all()


class Game(models.Model):
    Meta = meta("Jeu")
    name = models.CharField(verbose_name="nom", max_length=255, null=False, unique=True)
    notes = models.TextField(verbose_name="notes", max_length=512, null=False)
    box_img = models.CharField(verbose_name="url image boîte", max_length=2048, null=False)
    box_content_img = models.CharField(verbose_name="url image boîte contenu", max_length=2048, null=False)
    min_number_of_player = models.IntegerField(verbose_name="nombre de joueur minimum", null=False)
    max_number_of_player = models.IntegerField(verbose_name="nombre de joueur maximum", null=False)
    min_duration = models.IntegerField(verbose_name="durée minimum (minutes)", null=False)
    max_duration = models.IntegerField(verbose_name="durée maximum (minutes)", null=False)

    editor = models.ForeignKey(Editor, models.PROTECT, verbose_name="éditeur", null=False)
    tag = models.ForeignKey(Tag, models.PROTECT, verbose_name="tag", null=True)

    levels: "models.ManyToManyField[Level, Game]" = models.ManyToManyField(Level, verbose_name="niveau de jeu")
    types: "models.ManyToManyField[Type, Game]" = models.ManyToManyField(Type, verbose_name="type de jeu")
    genres: "models.ManyToManyField[Genre, Game]" = models.ManyToManyField(Genre, verbose_name="genre de jeu")
    ambiances: "models.ManyToManyField[Ambiance, Game]" = models.ManyToManyField(
        Ambiance, verbose_name="ambiance de jeu"
    )

    def __str__(self) -> str:
        return self.name

    @classmethod
    def init(
        cls,
        name: str,
        notes: str,
        box_img: str,
        box_content_img: str,
        min_number_of_player: int,
        max_number_of_player: int,
        min_duration: int,
        max_duration: int,
        editor: Editor,
        tag: Tag | None,
    ):
        return cls(
            name=name,
            notes=notes,
            box_img=box_img,
            box_content_img=box_content_img,
            min_number_of_player=min_number_of_player,
            max_number_of_player=max_number_of_player,
            min_duration=min_duration,
            max_duration=max_duration,
            editor=editor,
            tag=tag,
        )

    def clean(self) -> None:
        if self.min_duration < 0 or self.min_duration > self.max_duration:
            raise ValidationError("durée invalide")
        if self.min_number_of_player < 0 or self.min_number_of_player > self.max_number_of_player:
            raise ValidationError("nombre de joueur invalide")
        super().clean()

    @classmethod
    def all(cls):
        return cls.objects.order_by("name").all()

    @classmethod
    def search(cls, players: int, duration: int, level: str, type: str, ambiances: list[str], genres: list[str]):
        return cls.objects.order_by("name").filter(
            min_number_of_player__lte=players,
            max_number_of_player__gte=players,
            min_duration__lte=duration,
            max_duration__gte=duration,
            levels__name=level,
            types__name=type,
            ambiances__name__in=ambiances,
            genres__name__in=genres,
        )

    def number_of_player(self):
        if self.min_number_of_player == self.max_number_of_player:
            if self.min_number_of_player == 1:
                return "1 joueur"
            return f"{self.min_number_of_player} joueurs"
        return f"{self.min_number_of_player} à {self.max_number_of_player} joueurs"

    def duration(self):
        if self.min_duration == self.max_duration:
            return f"{self.min_duration} minutes"
        return f"{self.min_duration}-{self.max_duration} minutes"

    def genre_names(self):
        return ", ".join([i.name.capitalize() for i in self.genres.order_by("name").all()])

    def ambiance_names(self):
        return ", ".join([i.name.capitalize() for i in self.ambiances.order_by("name").all()])
