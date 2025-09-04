FROM python:3.9-slim

# Configuración del entorno
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r backend/requirements.txt

# Exponer los puertos necesarios
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["sh", "-c", "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000"]
