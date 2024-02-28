FROM python:3.12.2-slim-bookworm

RUN mkdir /app

COPY ./requarements.txt ./requarements.txt
RUN pip install -r ./requarements.txt
WORKDIR /app

COPY . /app
