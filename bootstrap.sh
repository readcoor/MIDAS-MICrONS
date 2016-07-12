#!/usr/bin/env bash

# This script provisions a blank CentOS 7 box for Microns
ln -s /vagrant /home/vagrant/sync

# updates CentOS
yum -y update

# Install basic stuff
yum -y install curl git unzip ntp emacs-nox libcurl-devel binutils gcc-c++ epel-release
yum -y install gdal-devel gdal geos 
yum -y install python-devel gcc postgresql94-server postgresql94-devel postgresql-contrib 
yum -y install postgresql-devel

# sync clock
chkconfig ntpd on
ntpdate time.apple.com

# install pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
rm get-pip.py

# install python libraries
pip install virtualenv
pip install awsebcli
pip install django
pip install django-rest-swagger
pip install markdown
pip install psycopg2
