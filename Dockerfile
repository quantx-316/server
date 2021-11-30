FROM python:3.7
WORKDIR /main 
COPY ./requirements.txt /main/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /main/requirements.txt

# Setup Ingest
RUN apt-get -y install -qq cron dos2unix
COPY ./ingest/* /main/ingest/
RUN apt-get update
COPY ./ingest/crontab /etc/cron.d/ingest_crontab
RUN chmod 0644 /etc/cron.d/ingest_crontab
RUN crontab /etc/cron.d/ingest_crontab
# run init script
COPY ./app /main/app
COPY ./init.sh /main/init.sh
RUN dos2unix /main/init.sh
ENTRYPOINT ["bash", "/main/init.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]