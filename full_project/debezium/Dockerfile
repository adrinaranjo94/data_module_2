FROM maven:3.8.1-openjdk-11
WORKDIR /app
COPY . /app

# Compila el proyecto y empaqueta el archivo .jar
RUN mvn clean package

# Ejecuta el archivo .jar directamente después de compilar
CMD ["java", "-jar", "/app/target/java-quick-start-1.0-SNAPSHOT.jar"]
