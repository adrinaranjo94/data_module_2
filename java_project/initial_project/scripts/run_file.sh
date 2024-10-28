#!/bin/bash

# Compile hello world java with javac
docker exec java_hello_world javac /app/HelloWorld.java

# Execute compiled file
docker exec java_hello_world java -cp /app HelloWorld