FROM python:latest

WORKDIR /home/dockerws/db_streamer

COPY conf/backend_socket conf/backend_socket
COPY conf/frontend_socket conf/frontend_socket
COPY conf/db_streamer_conf.yaml conf
COPY db_streamer.py .
COPY requirements.txt .

EXPOSE 5559

RUN pip install -r requirements.txt
RUN mkdir logs
RUN touch logs/db_streamer.log
CMD ["python", "db_streamer.py"]