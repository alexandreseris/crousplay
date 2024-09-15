from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db import models

from games import models as appmodels


def is_submodel(v) -> bool:
    try:
        check = issubclass(v, models.Model) and v is not models.Model
        return check
    except Exception:
        return False


def unregister(model: type[models.Model]):
    try:
        admin.site.unregister(model)
    except Exception:
        pass


for var in appmodels.__dict__.values():
    if is_submodel(var):
        admin.site.register(var)


unregister(Group)
unregister(User)
