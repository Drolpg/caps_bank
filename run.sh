#!/bin/sh

run_and_prefix() {
  name=$1
  shift
  "$@" 2>&1 | while IFS= read -r line; do
    echo "[$name] $line"
  done
}

echo "Database Startup"
echo "====================="
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
echo "====================="

echo "Iniciando todos os serviços..."
echo "=============================="

run_and_prefix "Django" python manage.py runserver 0.0.0.0:8000 &
run_and_prefix "Celery Worker" celery -A caps_bank worker -l info &
run_and_prefix "Celery Beat" celery -A caps_bank beat -l info &

wait
