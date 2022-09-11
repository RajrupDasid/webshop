FROM python:3.9.10-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv env


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

