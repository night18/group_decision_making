#!/bin/sh

source /var/app/venv/*/bin/activate
python /var/app/current/manage.py showmigrations
python /var/app/current/manage.py migrate
python /var/app/current/manage.py createsu
python /var/app/current/manage.py collectstatic --noinput
echo "WSGIPassAuthorization On" >> ../wsgi.conf