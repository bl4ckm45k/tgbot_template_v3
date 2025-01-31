FROM python:3.12-slim

WORKDIR /usr/src/app/bot

COPY ./requirements.txt ./
COPY ./src ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
