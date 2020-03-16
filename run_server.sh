#!/usr/bin/env bash

set -e

function manage_app () {
    python manage.py collectstatic --noinput
    python manage.py migrate
}

function start_development() {
    # use django runserver as development server here.
    manage_app
    python manage.py runserver 0.0.0.0:8000
}

if [ "$DATABASE" = "driverbackend" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "db_postgres" "5432"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
# use development server
start_development