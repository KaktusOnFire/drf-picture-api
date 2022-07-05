FROM python:3.8.1-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY app/requirements.txt /app/

RUN apk update \
    && apk add --virtual build-deps gcc git musl-dev \
    && apk add --no-cache postgresql-dev \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt\
    && apk del build-deps \
    && rm -rf /var/cache/apk/*

COPY app/. /app/
