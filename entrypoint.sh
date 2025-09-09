#!/bin/sh
set -e

# Variáveis padrão (caso não estejam definidas)
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

echo "Aguardando PostgreSQL em $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "PostgreSQL não disponível ainda, aguardando..."
  sleep 1
done
echo "PostgreSQL pronto!"

echo "Aguardando Redis em $REDIS_HOST:$REDIS_PORT..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  echo "Redis não disponível ainda, aguardando..."
  sleep 1
done
echo "Redis pronto!"

# Aplicar migrações e coletar arquivos estáticos
echo "Aplicando migrações e coletando arquivos estáticos..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Iniciar serviço apropriado
case "$1" in
  celery)
    echo "Iniciando Celery Worker..."
    exec celery -A caps_bank worker -l info
    ;;
  celery-beat)
    echo "Iniciando Celery Beat..."
    exec celery -A caps_bank beat -l info
    ;;
  *)
    echo "Iniciando Gunicorn..."
    exec gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3
    ;;
esac
