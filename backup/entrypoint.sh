#!/bin/sh

GIT="https://raw.githubusercontent.com/lordslair/nacridan-retriever-backend/master"

echo "`date +"%F %X"` Building shell dependencies and system set-up ..."

apk update \
    && apk add --no-cache rsync \
                          openssh \
                          sshpass \
                          bash \
                          zip \
    && apk add --no-cache --virtual .build-deps \
                                    tzdata \
    && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
    && apk del .build-deps \
    && wget "$GIT/backup/cron-backup-sh.daily"   -O /etc/periodic/hourly/cron-backup-sh  \
    && wget "$GIT/backup/cron-backup-sh.hourly"  -O /etc/periodic/daily/cron-backup-sh   \
    && wget "$GIT/backup/cron-backup-sh.monthly" -O /etc/periodic/monthly/cron-backup-sh \
    && chmod 755 /etc/periodic/*/cron-backup-sh \

echo "`date +"%F %X"` Build done ..."

exec /usr/sbin/crond -l2 -f
