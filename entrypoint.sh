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

# Remove a criação do superusuário
# echo "Verificando superusuário..."
# python manage.py shell << EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
#     User.objects.create_superuser(
#         username="${DJANGO_SUPERUSER_USERNAME}",
#         password="${DJANGO_SUPERUSER_PASSWORD}",
#         email="${DJANGO_SUPERUSER_EMAIL}",
#         cpf="${DJANGO_SUPERUSER_CPF}"
#     )
# EOF

exec "$@"
