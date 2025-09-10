#!/bin/sh
set -e

echo "Aguardando banco de dados..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Banco pronto!"

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

if [ "$1" = "api" ]; then
    echo "Iniciando API com Gunicorn..."
    exec gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
elif [ "$1" = "celery" ]; then
    echo "Iniciando Celery Worker..."
    exec celery -A caps_bank worker -l info
elif [ "$1" = "celery-beat" ]; then
    echo "Iniciando Celery Beat..."
    exec celery -A caps_bank beat -l info
else
    exec "$@"
fi
