# Imagen base ligera
FROM python:3.11-slim

# Evita generar archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando para correr la app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]