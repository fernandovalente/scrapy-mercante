FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN webdrivermanager firefox --linkpath /usr/local/bin

COPY ./src /app

ENV PATH = $PATH/:/app/scraper/geckodriver 
