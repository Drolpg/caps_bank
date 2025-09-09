FROM python:3.12-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar projeto
COPY . .

# Expor porta
EXPOSE 8000

# Comando de inicialização
RUN chmod +x run.sh
CMD ["./run.sh"]
