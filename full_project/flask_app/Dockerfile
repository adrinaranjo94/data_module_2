FROM python:3.8-slim

WORKDIR /app
COPY . /app

# Instala las dependencias de Flask y otras bibliotecas necesarias
RUN pip install -r requirements.txt

# Ejecuta la aplicación Flask
CMD ["python", "app.py"]
