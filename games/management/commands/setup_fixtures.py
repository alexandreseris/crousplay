from typing import TypeVar

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Model

from games import models

M = TypeVar("M", bound=Model)


def save(model: M) -> M:
    model.save()
    return model


class Command(BaseCommand):
    def handle(self, **options) -> None:
        with transaction.atomic():
            debutant = save(models.Level.init("débutant", 0))
            expert = save(models.Level.init("expert", 1))

            compet = save(models.Type.init("compétitif", 0))
            coop = save(models.Type.init("coppératif", 1))

            good_vides = save(models.Ambiance.init("bonne ambiance"))
            calme = save(models.Ambiance.init("calme"))

            bluff = save(models.Genre.init("bluff", "quand tu fais semblant"))
            draft = save(models.Genre.init("draft", "ça pioche des cartes"))
            negoc = save(models.Genre.init("négociation", "pour les marchands"))

            blue_cocker = save(models.Editor.init("Blue Cocker"))
            repos = save(models.Editor.init("Repos Production"))

            two_player = save(models.Tag.init("Bien pour deux joueurs"))
            noob_friendly = save(models.Tag.init("Parfait pour les débutants"))

            monopoly = save(
                models.Game.init(
                    name="Monopoly",
                    notes="",
                    box_img="https://www.hasbro.com/common/productimages/fr_FR/7EABAF9750569047F5778F4663C79E75/0ed5ef3ffbeebb69ce9074a3f66243a1833f8a7e.jpg",
                    box_content_img="https://www.hasbro.com/common/productimages/fr_FR/7EABAF9750569047F5778F4663C79E75/51e89be62bceecc45e75dba94880d89127f681fb.jpg",
                    min_number_of_player=0,
                    max_number_of_player=100,
                    min_duration=0,
                    max_duration=100,
                    editor=blue_cocker,
                    tag=None,
                )
            )
            monopoly.levels.add(debutant)
            monopoly.types.add(compet)
            monopoly.genres.add(negoc)
            monopoly.ambiances.add(calme)
            codenames = save(
                models.Game.init(
                    name="Code Names",
                    notes="",
                    box_img="https://iello.fr/wp-content/uploads/2016/10/Codenames_Mockup-2019_FR-Light-740x1156.png",
                    box_content_img="https://upload.wikimedia.org/wikipedia/commons/b/b0/Codenames_board_game.jpg",
                    min_number_of_player=4,
                    max_number_of_player=4,
                    min_duration=30,
                    max_duration=30,
                    editor=repos,
                    tag=noob_friendly,
                )
            )
            codenames.levels.add(debutant)
            codenames.levels.add(expert)
            codenames.types.add(compet)
            codenames.types.add(coop)
            codenames.genres.add(negoc)
            codenames.genres.add(draft)
            codenames.ambiances.add(calme)
            codenames.ambiances.add(good_vides)
            dixit = save(
                models.Game.init(
                    name="Dixit",
                    notes="",
                    box_img="https://cdn.svc.asmodee.net/production-libellud/uploads/2021/12/caroussel-boite-dixit-mobile-1.png",
                    box_content_img="https://upload.wikimedia.org/wikipedia/commons/1/1b/Dixit_spiel_p_014.jpg",
                    min_number_of_player=4,
                    max_number_of_player=10,
                    min_duration=30,
                    max_duration=100,
                    editor=repos,
                    tag=two_player,
                )
            )
            dixit.levels.add(debutant)
            dixit.levels.add(expert)
            dixit.types.add(compet)
            dixit.types.add(coop)
            dixit.genres.add(bluff)
            dixit.ambiances.add(calme)
            dixit.ambiances.add(good_vides)
            terraforming_mars = save(
                models.Game.init(
                    name="Terrforming mars",
                    notes="Le meilleur jeu tkt",
                    box_img="https://cdn.shortpixel.ai/spai/q_lossy+ret_img+to_auto/fryxgames.se/wp-content/uploads/2023/08/TM.png",
                    box_content_img="https://cdn.shortpixel.ai/spai/q_lossy+ret_img+to_auto/fryxgames.se/wp-content/uploads/2023/11/TM-scaled.jpg",
                    min_number_of_player=4,
                    max_number_of_player=10,
                    min_duration=30,
                    max_duration=100,
                    editor=repos,
                    tag=two_player,
                )
            )
            terraforming_mars.levels.add(debutant)
            terraforming_mars.levels.add(expert)
            terraforming_mars.types.add(compet)
            terraforming_mars.types.add(coop)
            terraforming_mars.genres.add(bluff)
            terraforming_mars.ambiances.add(calme)
            terraforming_mars.ambiances.add(good_vides)
