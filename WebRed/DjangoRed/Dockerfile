FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN apt install gcc
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .
