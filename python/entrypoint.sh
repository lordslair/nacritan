#!/bin/sh

echo "`date +"%F %X"` Building Python dependencies and system set-up ..."

apk update --no-cache \
    && apk add --no-cache python3 \
    && apk add --no-cache --virtual .build-deps \
                                    python3-dev \
                                    libffi-dev \
                                    gcc \
                                    libc-dev \
                                    tzdata \
    && pip3 --no-cache-dir install -U Flask \
                                      mysql-connector-python \
    && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
    && apk del .build-deps

echo "`date +"%F %X"` Build done ..."

exec flask run
