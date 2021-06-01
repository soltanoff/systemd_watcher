FROM python:3.6.9
MAINTAINER Ilya Soltanov <piccadillable@gmail.com>
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /systemd_watcher/requirements.txt
WORKDIR /systemd_watcher
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -qq -y install apt-utils
RUN apt-get -qq -y install curl
RUN apt-get install  dbus libapparmor1 libdbus-1-3 libdbus-glib-1-2 libdbus-glib-1-dev-bin libdbus-glib-1-dev libdbus-1-dev
RUN pip install -r requirements.txt
COPY . /systemd_watcher
