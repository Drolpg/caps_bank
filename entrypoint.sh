#!/bin/sh

echo "===== Migrando banco e coletando estáticos ====="
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
echo "================================================="

# Inicia Gunicorn para servir Django
exec gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
