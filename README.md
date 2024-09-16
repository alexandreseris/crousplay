# crousplay

Appli web de recommandation de jeu de société

## Installation initiale

- créer un compte sur <https://www.pythonanywhere.com>
- créer une application  web sur le dashboard, avec configuration manuelle
- créer une console bash, et exécuter les commandes suivantes (certaines informations vous seront demandées pour la création de l'accès admin et vous devrez également noter la clef secrète générée):

```sh
cd "$HOME" && git clone "https://github.com/alexandreseris/crousplay.git" && cd crousplay && ./deploy.sh -i
```

- puis redémarrer l'application web depuis la page de configuration pythonanywhere

## Mise à jour

- créer/reprendre une console bash et exécuter les commandes suivantes:

```sh
cd "$HOME" && cd crousplay && ./deploy.sh
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

# pour les commandes python manage.py ..., pensez à faire source "$HOME/env_crousplay.sh" avant si vous etes sur le serveru pythonanywhere
```

### deploy.sh synthax

```sh
usage: ./deploy.sh [-h] [-t] [-i] [-l] [-s SECRET_KEY]
   -h: show this message and exit
   -t: enable test mode
   -i: enable init mode
   -l: enable sql querry logging
   -s SECRET_KEY: provide a custom secret key
```

### Environnement

```text
CROUSPLAY_SECRET_KEY: string => utilisé en interne par django, mettez une chaine aléatoire de 32 charactères par ex
CROUSPLAY_DB_FILE: string => chemin vers le fichier sqlite
CROUSPLAY_TEMPLATES_DIR: string => chemin vers le repertoire de templates de l'application
CROUSPLAY_DEBUG: true|false [false] => permet de lancer l'appli en mode debug
CROUSPLAY_LOG_SQL: true|false [false] => permet de logger les requetes SQL sur stdout
CROUSPLAY_DONT_GENERATE_ALLOWED_HOSTS: true|false [false] => à passer à true pour le dev
```
