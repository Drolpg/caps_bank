#!/bin/sh
set -e

# Esperar pelo banco e Redis
echo "Aguardando PostgreSQL e Redis..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

# Rodar migrações e coletar estáticos
echo "Aplicando migrações e coletando arquivos estáticos..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Iniciar serviço apropriado
if [ "$1" = "celery" ]; then
    echo "Iniciando Celery Worker..."
    celery -A caps_bank worker -l info
elif [ "$1" = "celery-beat" ]; then
    echo "Iniciando Celery Beat..."
    celery -A caps_bank beat -l info
else
    echo "Iniciando Gunicorn..."
    gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
