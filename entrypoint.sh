#!/bin/bash
# Espera o banco de dados
echo "Aguardando banco de dados..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Banco pronto!"

# Aplicar migrações
python manage.py migrate --noinput

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
exec gunicorn caps_bank.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info
