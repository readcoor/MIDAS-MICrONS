#!/usr/bin/env bash

cd ~/sync
django-admin.py startproject microns_project
cd microns_project
touch db.sqlite3
chmod 666 db.sqlite3
pip freeze > requirements.txt
mkdir .ebextensions
cd .ebextensions
cat >django.config <<EOF
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: microns_project/wsgi.py
EOF

echo
echo
echo "# run the django server:"
echo "$ cd ~/root/dev/microns_project"
echo "$ python manage.py runserver '0.0.0.0:8000'"
echo
echo "# visit http://localhost:8080"
echo
