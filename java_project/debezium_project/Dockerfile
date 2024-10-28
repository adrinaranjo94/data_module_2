FROM maven:3.8.5-openjdk-17 AS maven_build

WORKDIR /app/

COPY app /app/

EXPOSE 8080

CMD ["mvn", "spring-boot:run"]
