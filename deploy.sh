#!/usr/bin/env bash

WSGI_FILE="/var/www/$(whoami)_pythonanywhere_com_wsgi.py"

cd /var/www/crousplay

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MISE A JOUR DEPUIS DEPOT DISTANT"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
git pull --depth 1

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- INSTALLATION DES DEPENDANCES"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
pip3.10 install .  # no venv, yolo

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MIGRATION BASE DE DONNEE"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
python3.10 manage.py migrate

if [ -z "$CROUSPLAY_SECRET_KEY" ]; then
    export CROUSPLAY_SECRET_KEY=$(openssl rand -hex 32)
    echo "CROUSPLAY_SECRET_KEY='$CROUSPLAY_SECRET_KEY'" > ~/.bashrc
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    echo "Une clef secrète a été générée, veuillez la noter et la conserver: $CROUSPLAY_SECRET_KEY"
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
fi

if [ -z "$CROUSPLAY_SU_CREATED" ]; then
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    echo "Super utilisateur inexistant, le programme de création d'utilisateur va être lancé"
    echo "Merci de répondre aux questions et bien prendre note de l'utilisateur et mot de passe qui sera utilisable pour l'accès à la page /admin"
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    python manage.py createsuperuser
    export CROUSPLAY_SU_CREATED="TRUE"
    echo "CROUSPLAY_SECRET_KEY='TRUE'" > ~/.bashrc
fi

cd ..
cat > "$WSGI_FILE" <<EOF
from crousplay.wsgi import application
EOF