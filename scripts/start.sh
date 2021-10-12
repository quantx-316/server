#!/bin/bash 

docker build -t server . && docker run -d --name server -p 80:80 server