FROM openjdk-17
WORKDIR /app
COPY target/myapp.jar myapp.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","myapp.jar"]
