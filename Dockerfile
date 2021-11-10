FROM python:3.7
WORKDIR /main 
COPY ./requirements.txt /main/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /main/requirements.txt
COPY ./app /main/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]