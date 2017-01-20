# First-time setup of postgres database in a development vm

For dev credential declarations, see `DATABASES` inside `django/microns/settings.py`. 

On your dev machine, `.bashrc` should set the dev flag:  
~~~bash
export DJANGO_DEV=1
~~~

Production values are stored in environment variables: `RDS_DB_NAME, RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT.`

## Set up `tester` user and `microns` database.

User `postgres` may not have access to current directory. If so, `cd /tmp` first before trying this.

~~~sql
$ sudo -u postgres psql template1  
template1=# create database microns;  
template1=# CREATE USER tester WITH PASSWORD 'test_password';  
template1=# GRANT ALL PRIVILEGES ON DATABASE "microns" to tester;  
template1=# ALTER ROLE tester SUPERUSER;  
template1=# \connect microns;  
microns=# CREATE EXTENSION postgis;
~~~



## (optional) Allow local access without passwords. 

Edit `pg_hba.conf` 

~~~bash
$ sudo emacs /var/lib/pgsql/9.4/data/pg_hba.conf
~~~

Look for existing lines like this:
~~~bash
# "local" is for Unix domain socket connections only                                                                                          
local   all  all      peer
# IPv4 local connections:                                                                                                                     
host    all  all 127.0.0.1/32 ident
# IPv6 local connections:                                                                                                                     
host    all  all ::1/128  ident
~~~

Change `peer` or `ident` -> `trust`

Add line to listen to 10.* subnet:  
`host    all    all    10.0.0.0/16   trust`

Restart so changes will take effect.

~~~~bash
$ sudo service postgresql-9.4 restart
~~~~


## Add address to listen to:  

~~~bash
$ sudo emacs /var/lib/pgsql/9.4/data/postgresql.conf
~~~

add `listen_addresses = '0.0.0.0'`

Restart so changes will take effect.

~~~bash
$ sudo service postgresql-9.4 restart
~~~

## Test: connect client to server

~~~bash
$ psql -d microns -h localhost -U tester  
microns=>
~~~
