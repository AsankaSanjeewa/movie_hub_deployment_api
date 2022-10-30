# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .

COPY start.sh /app/start.sh
RUN chmod +x start.sh
entrypoint "start.sh"
