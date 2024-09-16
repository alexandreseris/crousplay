#!/usr/bin/env bash


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
while getopts "htils:" opt; do
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
        *)
            usage
            ;;
    esac
done

pushd /var/www/crousplay || exit 1

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- Mise a jour depuis depot distant"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
git pull

./_deploy_app.sh "$@"

popd || exit 1
