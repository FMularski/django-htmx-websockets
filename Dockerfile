FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt

COPY . /code/