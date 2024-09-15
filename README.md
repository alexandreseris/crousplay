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
