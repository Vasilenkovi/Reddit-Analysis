#FROM python:3.10
#WORKDIR /WebRed

#ENV PYTHONBUFFERD=1
#RUN pip install --upgrade pip

#COPY ./requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#COPY gunicorn.socket /etc/systemd/system/
#COPY gunicorn.service /etc/systemd/system/
#EXPOSE 80
#RUN systemctl start gunicorn.socket 
#RUN systemctl enable gunicorn.socket
#RUN systemctl daemon-reload
#RUN systemctl restart gunicorn
#CMD ["systemctl", "start", "gunicorn.socket"]
#CMD ["systemctl", "enable", "gunicorn.socket"]
#CMD ["systemctl", "daemon-reload"]
#CMD ["systemctl", "restart", "gunicorn"]
# start from an official image
FROM python:3.10

# рабочая директория внутри проекта
WORKDIR /usr/src/WebRed

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем содержимое текущей папки в контейнер
COPY . .
