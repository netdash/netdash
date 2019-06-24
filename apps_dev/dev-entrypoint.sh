#!/usr/bin/env bash

set -e

cd ../..

for app in $(ls -d apps_dev/*/); do
    pip install -e ${app} || echo "$(basename ${0}): couldn't install ${app}"
done

cd src/netdash
exec ../../docker-entrypoint.sh "${@}"
