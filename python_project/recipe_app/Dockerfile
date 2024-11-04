# Dockerfile
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará la aplicación Flask
EXPOSE 5050

# Comando de inicio de la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
