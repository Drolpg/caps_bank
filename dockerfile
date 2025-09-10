# Base image
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema necessárias
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo o projeto
COPY . .

# Expor porta 8000
EXPOSE 8000

# Comando padrão (definido no docker-compose)
CMD ["gunicorn", "caps_bank.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
