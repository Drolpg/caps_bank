#!/bin/sh
set -e

echo "Esperando pelo banco de dados..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Esperando pelo Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 1
done

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

exec "$@"
