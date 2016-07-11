#!/usr/bin/env bash

# This script provisions a blank CentOS box for Microns
ln -s /vagrant /home/vagrant/sync

# updates CentOS
yum -y update

# Install basic stuff
#sudo rpm -ivh http://yum.postgresql.org/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-2.noarch.rpm

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

# install GDAL
#cd /tmp
#curl -O http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz
#tar xzf gdal-2.1.0.tar.gz 
#cd gdal-2.1.0/
#./configure
#make
#make install

# install Geos
# see https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/geolibs/
#cd /tmp
#curl -O http://download.osgeo.org/geos/geos-3.5.0.tar.bz2
#tar xjf geos-3.5.0.tar.bz2
#cd geos-3.5.0
#./configure
#make
#make install

