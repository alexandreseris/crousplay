from collections.abc import Sequence

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Model

from games import models


class Command(BaseCommand):
    def handle(self, **options) -> None:
        with transaction.atomic():
            models_: Sequence[type[Model]] = [
                models.Game,
                models.Level,
                models.Type,
                models.Ambiance,
                models.Genre,
                models.Editor,
                models.Tag,
            ]
            for m in models_:
                m.objects.all().delete()  # type: ignore[attr-defined]
