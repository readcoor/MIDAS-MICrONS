#!/usr/bin/env bash

# This sets up an empty django project.
#
# You probably don't need to run this script, since the files
# it creates are already checked into this git repo.

cd ~/sync
django-admin.py startproject microns
cd microns
touch db.sqlite3
chmod 666 db.sqlite3
pip freeze > requirements.txt
mkdir .ebextensions
cd .ebextensions
cat >django.config <<EOF
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: microns/wsgi.py
EOF

echo
echo
echo "# run the django server:"
echo "$ cd ~/sync/django"
echo "$ python manage.py runserver '0.0.0.0:8000'"
echo
echo "# visit http://localhost:8080"
echo
