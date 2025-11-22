# Usa uma imagem leve do Python
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia todos os seus arquivos para dentro do container
COPY . .

# Instala as bibliotecas do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o site usando Gunicorn na porta que o Google der ($PORT)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_flask:app