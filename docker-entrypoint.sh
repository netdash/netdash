#!/usr/bin/env bash

set -e

pipenv run python manage.py migrate

exec "${@}"
