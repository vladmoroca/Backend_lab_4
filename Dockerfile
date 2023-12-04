FROM python:3.10.11-slim-bullseye

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /base

WORKDIR /base

ENV FLASK_APP=base/__init__

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD flask run -h 0.0.0.0 -p $PORT
