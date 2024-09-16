#!/usr/bin/env bash

set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

REPO_DIR="$HOME/crousplay"
pushd "$REPO_DIR" || exit 1

echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
echo "-- Mise a jour depuis depot distant"
echo "----------------------------------------------------------"
echo "----------------------------------------------------------"
git pull

./_deploy_app.sh "$@"

popd || exit 1
