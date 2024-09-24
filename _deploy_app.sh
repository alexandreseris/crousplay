#!/usr/bin/env bash

set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

usage() {
    echo "usage: $0 [-h] [-t] [-i] [-l] [-s SECRET_KEY]"
    echo "   -h: show this message and exit"
    echo "   -t: enable test mode"
    echo "   -i: enable init mode"
    echo "   -l: enable sql querry logging"
    echo "   -s SECRET_KEY: provide a custom secret key"
    exit 1
}

is_test=0
is_init=0
log_sql=0
secret_key=""
su_user=""
su_password=""
su_email=""
while getopts "htils:U:P:E:" opt; do
    case "$opt" in
        h)
            usage
            ;;
        t)  is_test=1
            ;;
        i)  is_init=1
            ;;
        l)  log_sql=1
            ;;
        s)  secret_key="$OPTARG"
            ;;
        U)  su_user="$OPTARG"
            ;;
        P)  su_password="$OPTARG"
            ;;
        E)  su_email="$OPTARG"
            ;;
        *)
            usage
            ;;
    esac
done

REPO_DIR="$HOME/crousplay"
SOURCE_ENV_FILE="$HOME/env_crousplay.sh"
STATIC_DIR="$HOME/crousplay_static"
DB_FILE="$REPO_DIR/db.sqlite3"
TEMPLATES_DIR="$REPO_DIR/games/templates"
WSGI_FILE="/var/www/$(whoami)_pythonanywhere_com_wsgi.py"

pushd "$HOME/crousplay" || exit 1

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- Installation/mise a jour des dependances"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
pip3.10 install .  # no venv, yolo

if [[ "$is_init" == 1 ]]; then
    if [[ -z "$secret_key" ]]; then
        secret_key=$(openssl rand -hex 32)
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        echo "/!\ Une clef secrète a été générée, veuillez la noter et la conserver /!\ : $secret_key"
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
    fi

    if [ ! -d "$STATIC_DIR" ]; then
        mkdir -p $STATIC_DIR
    fi

    if [ -f "$WSGI_FILE" ]; then
        rm "$WSGI_FILE"
    fi
    if [ -f "$SOURCE_ENV_FILE" ]; then
        rm "$SOURCE_ENV_FILE"
    fi

    echo "import os" >> "$WSGI_FILE"
    echo "os.environ['CROUSPLAY_SECRET_KEY'] = '$secret_key'" >> "$WSGI_FILE"
    echo "os.environ['CROUSPLAY_STATIC_DIR'] = '$STATIC_DIR'" >> "$WSGI_FILE"
    echo "export CROUSPLAY_SECRET_KEY='$secret_key'" >> "$SOURCE_ENV_FILE"
    echo "export CROUSPLAY_STATIC_DIR='$STATIC_DIR'" >> "$SOURCE_ENV_FILE"
    if [[ "$is_test" == 1 ]]; then
        echo "export CROUSPLAY_DEBUG='true'" >> "$SOURCE_ENV_FILE"
        echo "os.environ['CROUSPLAY_DEBUG'] = 'true'" >> "$WSGI_FILE"
    fi
    if [[ "$log_sql" == 1 ]]; then
        echo "export CROUSPLAY_LOG_SQL='true'" >> "$SOURCE_ENV_FILE"
        echo "os.environ['CROUSPLAY_LOG_SQL'] = 'true'" >> "$WSGI_FILE"
    fi
    echo "export CROUSPLAY_DB_FILE='$DB_FILE'" >> "$SOURCE_ENV_FILE"
    echo "export CROUSPLAY_TEMPLATES_DIR='$TEMPLATES_DIR'" >> "$SOURCE_ENV_FILE"
    chmod +x "$SOURCE_ENV_FILE"
    echo "os.environ['CROUSPLAY_DB_FILE'] = '$DB_FILE'" >> "$WSGI_FILE"
    echo "os.environ['CROUSPLAY_TEMPLATES_DIR'] = '$TEMPLATES_DIR'" >> "$WSGI_FILE"
    echo "from crousplay.wsgi import application" >> "$WSGI_FILE"
fi

source "$SOURCE_ENV_FILE"

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- Création/maj des fichiers statiques"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
python3.10 manage.py collectstatic

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- Migration base de donnee"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
python3.10 manage.py migrate

if [[ "$is_init" == 1 ]]; then
    if [[ "$is_test" == 1 ]]; then
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        echo "-- Création des fixtures"
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        python3.10 manage.py setup_fixtures
    fi
    if [[ ! -z "$su_user" ]] && [[ ! -z  "$su_password" ]] && [[ ! -z "$su_email" ]]; then
        export DJANGO_SUPERUSER_USERNAME="$su_user"
        export DJANGO_SUPERUSER_PASSWORD="$su_password"
        export DJANGO_SUPERUSER_EMAIL="$su_email"
        python3.10 manage.py createsuperuser --noinput
    else
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        echo "/!\ Création de l'utilisateur admin /!\\"
        echo "Merci de répondre aux questions et bien prendre note de l'utilisateur et mot de passe qui sera utilisable pour l'accès à la page /admin"
        echo "----------------------------------------------------------"
        echo "----------------------------------------------------------"
        python3.10 manage.py createsuperuser
    fi
fi

popd || exit 1
