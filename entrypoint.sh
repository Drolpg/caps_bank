#!/bin/sh
set -e

echo "=============================="
echo "Aplicando migrações Django..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
echo "=============================="

# Inicia Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
