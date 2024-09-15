#!/usr/bin/env bash

WSGI_FILE="/var/www/$(whoami)_pythonanywhere_com_wsgi.py"

if [ -z "$1" ]; then
    IS_INIT=0
else
    IS_INIT=1
fi

pushd /var/www/crousplay

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MISE A JOUR DEPUIS DEPOT DISTANT"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
git pull --depth 1

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- INSTALLATION/MISE A JOUR DES DEPENDANCES"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
pip3.10 install .  # no venv, yolo

if [[ "$IS_INIT" == 1 ]]; then
    CROUSPLAY_SECRET_KEY=$(openssl rand -hex 32)
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    echo "Une clef secrète a été générée, veuillez la noter et la conserver: $CROUSPLAY_SECRET_KEY"
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"

    rm $WSGI_FILE 2> /dev/null
    echo "import os" >> $WSGI_FILE
    echo "os.environ['CROUSPLAY_SECRET_KEY'] = '$CROUSPLAY_SECRET_KEY'" >> $WSGI_FILE
    echo "from crousplay.wsgi import application" >> $WSGI_FILE
fi

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MIGRATION BASE DE DONNEE"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
python3.10 manage.py migrate

if [[ "$IS_INIT" == 1 ]]; then
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    echo "Super utilisateur inexistant, le programme de création d'utilisateur va être lancé"
    echo "Merci de répondre aux questions et bien prendre note de l'utilisateur et mot de passe qui sera utilisable pour l'accès à la page /admin"
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    python manage.py createsuperuser
fi

popd
