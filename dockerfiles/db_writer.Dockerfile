FROM python:latest

WORKDIR /home/dockerws/db_writer

COPY conf/backend_socket conf/backend_socket
COPY conf/db conf/db
COPY conf/db_writer_conf.yaml conf
COPY ORM.py .
COPY db_writer.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN mkdir logs
RUN touch logs/db_writer.log
CMD ["python", "db_writer.py"]