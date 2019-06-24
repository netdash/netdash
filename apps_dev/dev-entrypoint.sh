#!/usr/bin/env bash

set -e

echo $(pwd)
for app in $(ls -d ../../apps_dev/*/); do
    pip install -e ${app} || echo "couldn't install ${app}"
done

exec ../../docker-entrypoint.sh "${@}"
