#!/bin/bash
set -e

echo "Running Migrations"
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Start Gunicorn"
exec gunicorn src.core.wsgi:application --bind 0.0.0.0:8000