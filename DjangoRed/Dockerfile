FROM python:3.10
WORKDIR /usr/src/WebRed
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements_linux.txt .
RUN pip install -r requirements_linux.txt
COPY . .
