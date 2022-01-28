#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

# fix celery log access
mkdir -p '/var/log/celery/'
chown -R $uid:$gid '/var/log/celery/'

uid=root
gid=root

if [ $DEBUG = True ]; then
    python3 manage.py timeside-celery-worker --loglevel $log_level --logfile $worker_log_file --uid $uid --gid $gid
else
    celery -A worker worker --loglevel=$log_level --logfile=$worker_log_file --uid=$uid --gid=$gid
fi

