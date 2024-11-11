FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=weather

# Copia el archivo init.sql para inicializar la base de datos y tablas
COPY init.sql /docker-entrypoint-initdb.d/