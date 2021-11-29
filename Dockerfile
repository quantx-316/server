FROM python:3.7
WORKDIR /main 
COPY ./requirements.txt /main/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /main/requirements.txt

# Setup Ingest
COPY ./ingest/* /main/ingest/
RUN apt-get update
RUN apt-get -y install -qq cron
# RUN python /main/ingest/fast_forward.py
COPY ./ingest/crontab /etc/cron.d/ingest_crontab
RUN chmod 0644 /etc/cron.d/ingest_crontab
RUN crontab /etc/cron.d/ingest_crontab


COPY ./app /main/app
COPY ./init.sh /main/init.sh
ENTRYPOINT ["bash", "/main/init.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]