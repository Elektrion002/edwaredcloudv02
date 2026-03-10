# Usar una imagen oficial de Python ligera
FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del subsistema
COPY . .

# Exponer el puerto configurado (5001)
EXPOSE 5001

# Comando por defecto para correr con Gunicorn
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:5001", "--access-logfile", "-", "run:app"]
