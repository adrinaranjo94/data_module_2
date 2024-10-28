# Usa la imagen oficial de MySQL
FROM mysql:8.0

# Configura las variables de entorno
ENV MYSQL_ROOT_PASSWORD=MyNewPass
ENV MYSQL_DATABASE=customerdb
ENV MYSQL_USER=user_root
ENV MYSQL_PASSWORD=MyNewPass

ADD customer.sql /docker-entrypoint-initdb.d

# Expone el puerto de MySQL
EXPOSE 3306