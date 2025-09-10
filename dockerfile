# Base image
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema necessárias para psycopg2 e netcat
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar todo o projeto para dentro do container
COPY . .

# Garantir permissão de execução para o entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Variáveis de ambiente importantes
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expor porta 8000
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
