FROM python:3.6.9-alpine

WORKDIR /usr/src/rest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg 
RUN pip3 install -r requirements.txt 
RUN apk del build-deps

COPY . .
