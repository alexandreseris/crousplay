# crousplay

Appli web de recommandation de jeu de société

## Installation initiale

- créer un compte sur <https://www.pythonanywhere.com>
- créer une application  web sur le dashboard, avec configuration manuelle
- créer une console bash, et exécuter les commandes suivantes (certaines informations vous seront demandées pour la création de l'accès admin et vous devrez également noter la clef secrète générée):

```sh
cd /var/www && git clone --depth 1 -b "main" "https://github.com/alexandreseris/crousplay.git" && cd crousplay && ./deploy.sh init
```

- puis redémarrer l'application web depuis la page de configuration pythonanywhere

## Mise à jour

- créer/reprendre une console bash et exécuter les commandes suivantes:

```sh
cd /var/www && cd crousplay && ./deploy.sh
```

- puis redémarrer l'application web depuis la page de configuration pythonanywhere

## Notes

Si vous avez un compte gratuit pythonanywhere:

- pensez à cliquer sur le bouton `Run until 3 months from today` depuis la page de configuration de l'appli web tous les trois mois (ou moins)

## Dev

```sh
python -m venv venv # crée un environnement virtuel dans le dossier venv du répertoire courant
pip install --editable .[dev]  # installe les dépendances (dev compris) en mode éditable
python manage.py setup_fixtures  # créer les données de fixtures
python manage.py makemigrations games  # crée les migrations de bdd
python manage.py runserver  # lance le serveur de test
```

### Environnement

```text
CROUSPLAY_SECRET_KEY: string => utilisé en interne par django, mettez une chaine aléatoire de 32 charactères par ex
CROUSPLAY_DEBUG: true|false [false] => permet de lancer l'appli en mode debug
CROUSPLAY_LOG_SQL: true|false [false] => permet de logger les requetes SQL sur stdout
```
