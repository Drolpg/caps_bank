# Base image
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema necessárias para psycopg2
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo o projeto
COPY . .

# Dar permissão para run.sh (opcional, para dev)
# RUN chmod +x run.sh

# Expor porta 8000 para Django
EXPOSE 8000

# Comando padrão para produção
# Aplica migrações, coleta estáticos e inicia Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn caps_bank.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
