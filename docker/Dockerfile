FROM php:apache

RUN apt-get update \
    && apt-get install -y wget sqlite3 \
    && wget    https://github.com/lordslair/nacridan-retriever-backend/archive/master.zip -O /tmp/nrb.zip
    && unzip   /tmp/nrb.zip -d /tmp/
    && cp -a   /tmp/nacridan-retriever-backend-master/code/* /var/www/html
    && sqlite3 /var/www/html/nacridan.db < /var/www/html/data/initDB.SQL
    && rm -rf  /tmp/nacridan-retriever-backend-master
    && rm -rf  /tmp/nrb.zip

EXPOSE 80
