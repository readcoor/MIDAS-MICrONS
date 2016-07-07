This spins up a Vagrant instance of a Microns development VM.

## Install
Clone [this repo](https://github.com/WyssMICrONS/api-server) and `cd` into it.  
Download and install [Vagrant](https://www.vagrantup.com/downloads.html), then run these steps:
 `$ vagrant init centos/7`  
 `$ vagrant plugin install vagrant-vbguest`  
 `$ vagrant up`  
 `$ vagrant ssh`  

## How to

How to save a running vagrant VM as a new template (default name package.box)  
$ `vagrant package`  
Make a new directory and mv package.box into it. Then run these steps:  
$ `vagrant init package.box`  
$ `vagrant up`  

## Run django on your local machine

 `$ vagrant ssh`  
 Run these commands on your vagrant VM:  
 `$ cd ~/sync/django`  
 `$ python manage.py runserver '0.0.0.0:8000'`  

  visit `http://localhost:8080`  
  visit [API browser](http://localhost:8080/docs/), written with [swagger](http://swagger.io/)  

## Testing
  Run django on your local machine, then run these steps:  
  `$ cd ~/sync/django/`  
  `$ python manage.py test`  

## Configure your vagrant VM with your AWS ElasticBeanstalk client
  [Deploying Django on Beanstalk](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)  
  Configure your [API credentials](https://console.aws.amazon.com/iam/home#users)  
 `$ eb init -p python2.7 api`  
 `$ eb init`  
  

## Manage django on AWS instance
  SSH into linux VM with this command:  
  `$ eb ssh`  
  Then manage django with this:  
  `$ /opt/python/run/venv/bin/python /opt/python/current/app/manage.py <command>`
