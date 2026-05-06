# Backend Dockerfile - Django
FROM python:3.11-slim

WORKDIR /app

#comentario de pruebas en el docker

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
