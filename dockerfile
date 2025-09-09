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

# Copiar entrypoint e dar permissão
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expor porta 8000 para Django
EXPOSE 8000

# Comando padrão
ENTRYPOINT ["/entrypoint.sh"]
