#!/usr/bin/env bash

set -e

cd ../..

for app in $(ls -d apps_dev/*/); do
    app_name=$(grep "name=" ${app}/setup.py | sed -E -e "s/name=|[\'\,]//g" -e "s/[\-]/\_/g")
    modules=$(grep "NETDASH_MODULES=" .user-settings.env || grep "NETDASH_MODULES=" .defaults.env)

    if [[ $(echo "${modules}" | grep ${app_name}) ]]
    then
        pip3 install -e ${app} || echo "$(basename ${0}): couldn't install ${app}"
    fi

done

cd src/netdash
exec ../../docker-entrypoint.sh "${@}"
