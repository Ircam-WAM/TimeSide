#!/bin/bash

# paths
app='/srv/app'
src='/srv/src'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
log='/var/log/uwsgi/app.log'
worker_logfile='/var/log/celery/worker.log'
loglevel='DEBUG'

# uwsgi params
port=8000
processes=4
threads=4
autoreload=3
# uwsgi and celery params
uid='www-data'
gid='www-data'

# install more apps
# pip install -U django-cors-headers
# ...

# always take the last youtube-dl version
pip3 install -U youtube-dl

# always take the last youtube-dl version
pip3 install -U youtube-dl

# Install plugins
bash /srv/app/bin/setup_plugins.sh

# wait for other services
# bash $app/bin/wait.sh
