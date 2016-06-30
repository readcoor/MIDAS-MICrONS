#!/usr/bin/env bash

# This script provisions a blank CentOS box for Microns
ln -s /vagrant /home/vagrant/sync

# updates CentOS
yum -y update

# Install basic stuff
yum -y install curl git unzip emacs-nox
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
rm get-pip.py

# Install Django

pip install virtualenv
pip install awsebcli
pip install django
pip install django-rest-swagger
