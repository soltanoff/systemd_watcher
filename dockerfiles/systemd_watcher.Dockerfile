FROM python:3.5
MAINTAINER Ilya Soltanov <piccadillable@gamil.com>
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /systemd_watcher/requirements.txt
COPY ./wait-for-it.sh /systemd_watcher/wait-for-it.sh
WORKDIR /systemd_watcher
RUN chmod +x wait-for-it.sh
RUN pip install -r requirements.txt
COPY . /systemd_watcher
