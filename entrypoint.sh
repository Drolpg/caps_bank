#!/bin/sh
set -e

# Carregar variáveis do .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Rodando migrações e coletando arquivos estáticos..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
