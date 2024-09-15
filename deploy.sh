#!/usr/bin/env bash

WSGI_FILE="/var/www/$(whoami)_pythonanywhere_com_wsgi.py"

is_test=0
is_init=0
log_sql=0
secret_key=""
while getopts "htils:" opt; do
    case "$opt" in
        h)
            echo "usage: $0 [-h] [-t] [-i] [-l] [-s SECRET_KEY]"
            echo "   -h: show this message and exit"
            echo "   -t: enable test mode"
            echo "   -i: enable init mode"
            echo "   -l: enable sql querry logging"
            echo "   -s SECRET_KEY: provide a custom secret key"
            exit 0
            ;;
        t)  is_test=1
            ;;
        i)  is_init=1
            ;;
        l)  log_sql=1
            ;;
        s)  secret_key="$OPTARG"
            ;;
    esac
done

pushd /var/www/crousplay

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MISE A JOUR DEPUIS DEPOT DISTANT"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
git pull

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- INSTALLATION/MISE A JOUR DES DEPENDANCES"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
pip3.10 install .  # no venv, yolo

# mega sadge, j'arrive pas à inclure les fichiers html dans le package :(
mkdir --parents ~/.local/lib/python3.10/site-packages/games/templates/games 2> /dev/null
cp games/templates/games/*.html ~/.local/lib/python3.10/site-packages/games

if [[ "$is_init" == 1 ]]; then
    if [[ -z "$secret_key" ]]; then
        secret_key=$(openssl rand -hex 32)
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        echo "Une clef secrète a été générée, veuillez la noter et la conserver: $secret_key"
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
    fi

    rm $WSGI_FILE 2> /dev/null
    echo "import os" >> $WSGI_FILE
    echo "os.environ['CROUSPLAY_SECRET_KEY'] = '$secret_key'" >> $WSGI_FILE
    if [[ "$is_test" == 1 ]]; then
        echo "os.environ['CROUSPLAY_DEBUG'] = 'true'" >> $WSGI_FILE
    fi
    if [[ "$log_sql" == 1 ]]; then
        echo "os.environ['CROUSPLAY_LOG_SQL'] = 'true'" >> $WSGI_FILE
    fi
    echo "from crousplay.wsgi import application" >> $WSGI_FILE
fi

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- MIGRATION BASE DE DONNEE"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
python3.10 manage.py migrate

if [[ "$is_init" == 1 ]]; then
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    echo "Super utilisateur inexistant, le programme de création d'utilisateur va être lancé"
    echo "Merci de répondre aux questions et bien prendre note de l'utilisateur et mot de passe qui sera utilisable pour l'accès à la page /admin"
    echo "----------------------------------------------------------"
    echo "----------------------------------------------------------"
    python3.10 manage.py createsuperuser
fi

popd
