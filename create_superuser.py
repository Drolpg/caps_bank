import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")
cpf = os.getenv("DJANGO_SUPERUSER_CPF", "00000000000")  # CPF obrigatório

if not User.objects.filter(username=username).exists():
    print("Criando superusuário padrão...")
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        cpf=cpf,
    )
else:
    print("Superusuário já existe, pulando criação...")
