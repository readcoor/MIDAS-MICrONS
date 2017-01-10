#!/usr/bin/env bash

# This script provisions a blank CentOS 7 box for Microns
ln -s /vagrant /home/vagrant/sync

echo $'\nexport DJANGO_DEV=1' >> /home/vagrant/.bashrc
echo $'\nexport PATH=/usr/pgsql-9.4/bin:$PATH' >> /home/vagrant/.bashrc

# sync clock
chkconfig ntpd on
ntpdate time.apple.com

# updates CentOS
yum -y update

# Install basic stuff
yum -y install curl git unzip ntp emacs-nox libcurl-devel binutils gcc gcc-c++ epel-release
yum -y install python34 python34-devel 
yum -y install openssl-devel

# Install geography libraries
yum -y install gdal-devel gdal geos 

# Install postgres
yum -y localinstall https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-2.noarch.rpm
yum -y install postgis2_94 postgis2_94-devel postgresql94-server postgresql94-devel
#yum -y install postgresql94-server postgresql94-devel postgresql-contrib 
#yum -y install postgresql-devel

# needed for pip install psycopg2
ln -s /usr/pgsql-9.4/bin/pg_config /usr/bin/pg_config

# start postgres
cd /home/vagrant
/usr/pgsql-9.4/bin/postgresql94-setup initdb 
systemctl start postgresql-9.4
systemctl enable postgresql-9.4
chkconfig postgresql-9.4 on

# install pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py
rm get-pip.py

# install python libraries
pip install -r /home/vagrant/sync/django/requirements.txt
