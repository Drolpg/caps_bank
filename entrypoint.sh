#!/bin/sh
set -e

# Função para esperar pelo serviço
wait_for() {
  host="$1"
  port="$2"
  echo "Aguardando $host:$port..."
  while ! nc -z $host $port; do
    sleep 1
  done
  echo "$host:$port pronto!"
}

# Esperar pelo banco e Redis
wait_for $DB_HOST $DB_PORT
wait_for $REDIS_HOST $REDIS_PORT

# Executar comandos dependendo do container
if [ "$1" = "api" ]; then
    echo "Aplicando migrações e coletando arquivos estáticos..."
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    echo "Iniciando Gunicorn..."
    gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
elif [ "$1" = "celery" ]; then
    echo "Iniciando Celery Worker..."
    celery -A caps_bank worker -l info
elif [ "$1" = "celery-beat" ]; then
    echo "Iniciando Celery Beat..."
    celery -A caps_bank beat -l info
else
    echo "Comando desconhecido: $1"
    exit 1
fi
