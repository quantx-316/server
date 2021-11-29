#!/bin/bash

service cron start
# retry until db startup correctly...
n=0
sleep 10
until [ "$n" -ge 20 ]
do
   python /main/ingest/fast_forward.py && break 
   n=$((n+1)) 
   sleep 1
done
uvicorn app.main:app --host 0.0.0.0 --port 80
