FROM maven:3.8.5-openjdk-17

WORKDIR /app

COPY app/pom.xml .

RUN mvn dependency:go-offline -B

COPY app/src ./src

EXPOSE 8080

CMD ["mvn", "spring-boot:run"]
