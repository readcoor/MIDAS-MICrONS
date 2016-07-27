# First-time setup of postgres database in vagrant dev vm

For dev credential declarations, see `DATABASES` inside `django/microns/settings.py`.

First, set up `tester` user and `microns` database.

~~~~bash
$ sudo -u postgres psql template1  
template1=# create database microns;  
template1=# CREATE USER tester WITH PASSWORD 'test_password';  
template1=# GRANT ALL PRIVILEGES ON DATABASE "microns" to tester;  
template1=# ALTER ROLE tester SUPERUSER;  
template1=# \connect microns;  
microns=# CREATE EXTENSION postgis;
~~~~

(optional) Edit `pg_hba.conf` to allow local access without passwords. Look for
existing lines like this:
~~~
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

~~~~bash
$ sudo emacs /var/lib/pgsql/9.4/data/pg_hba.conf  
$ sudo service postgresql-9.4 restart
~~~~

Add address to listen to:  
`listen_addresses = '0.0.0.0'`

~~~~bash
$ sudo emacs /var/lib/pgsql/9.4/data/postgresql.conf
$ sudo service postgresql-9.4 restart
~~~~

Test: connect client to server

~~~~bash
$ psql -d microns -h localhost -U tester  
microns=>
~~~~
