#!/bin/sh

echo "`date +"%F %X"` Building Python dependencies and system set-up ..."

apk update --no-cache \
    && apk add --no-cache python3 \
                          py3-pip \
    && apk add --no-cache --virtual .build-deps \
                                    python3-dev \
                                    libffi-dev \
                                    gcc \
                                    libc-dev \
                                    tzdata \
    && pip --no-cache-dir install -U sqlite-web \
    && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
    && apk del .build-deps

echo "`date +"%F %X"` Build done ..."

exec sqlite_web --host=$FLASK_HOST \
                --port=$FLASK_PORT \
                --password \
                $SQLITE_DB_NAME
