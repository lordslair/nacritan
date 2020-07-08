#!/bin/sh

echo "`date +"%F %X"` Building Python dependencies and system set-up ..."

apk update --no-cache \
    && apk add --no-cache python3 \
                          libjpeg \
    && apk add --no-cache --virtual .build-deps \
                                    python3-dev \
                                    libffi-dev \
                                    gcc \
                                    libc-dev \
                                    jpeg-dev \
                                    zlib-dev \
                                    tzdata \
    && pip3 --no-cache-dir install -U Flask \
                                      Flask-cors \
                                      Flask-httpauth \
                                      Pillow-PIL \
                                      redis \
                                      pytest \
    && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
    && apk del .build-deps \
    && pytest /code/tests

echo "`date +"%F %X"` Build done ..."

echo "`date +"%F %X"` Loading Python scripts ..."
mkdir  /code && cd /code
wget   https://github.com/lordslair/nacridan-retriever-backend/archive/master.zip -O /tmp/nrb.zip &&
unzip  /tmp/nrb.zip -d /tmp/ &&
cp -a  /tmp/nacridan-retriever-backend-master/python/* /code/ &&
rm -rf /tmp/nacridan-retriever-backend-master &&
rm -rf /tmp/nrb.zip
echo "`date +"%F %X"` Loading done ..."

exec flask run --host=$FLASK_HOST \
               --port=$FLASK_PORT \
               $FLASK_DEBUG \
               $FLASK_THREAD
