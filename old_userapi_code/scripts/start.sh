#!/bin/bash 

docker build -t userapi . && docker run -d --name userapi -p 80:80 userapi 