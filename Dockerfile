FROM python:3.9-buster

WORKDIR /usr/src/blinder

COPY requirements.txt .
RUN pip install -r requirements.txt