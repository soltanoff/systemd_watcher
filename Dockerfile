FROM python:3.14-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV buildDeps=' \
        build-essential \
        musl-dev \
        gcc \
        apt-utils \
        curl \
        dbus \
        libapparmor1 \
        libdbus-1-3 \
        libdbus-glib-1-2 \
        libdbus-glib-1-dev-bin \
        libdbus-glib-1-dev \
        libdbus-1-dev \
    '

RUN apt-get update \
    && apt-get install -y $buildDeps --no-install-recommends \
    && pip install --upgrade --no-cache-dir pip wheel setuptools

# will be cached if no changes in this files
COPY requirements.txt /
COPY scripts/start.sh /

RUN chmod +x /start.sh

RUN pip install -r requirements.txt

COPY app /app

WORKDIR /app

CMD [ "../start.sh" ]
