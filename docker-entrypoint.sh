#!/usr/bin/env bash

set -e

python3 manage.py collectstatic --noinput
python3 manage.py migrate

exec "${@}"
