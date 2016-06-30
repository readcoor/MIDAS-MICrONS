This spins up a Vagrant instance of a Microns development VM.

## Install

Download and install [Vagrant](https://www.vagrantup.com/downloads.html)  
 `$ vagrant init centos/7`  
 `$ vagrant plugin install vagrant-vbguest`  
 `$ vagrant up`  
 `$ vagrant ssh`  

## How to

How to save a running vagrant VM as a new template (default name package.box)  
$ `vagrant package`  
Make a new directory and mv package.box into it  
$ `vagrant init package.box`  
$ `vagrant up`  

## Run django on your local machine

 `$ vagrant ssh`  
 Run these commands on your vagrant VM:  
 `$ cd ~/sync/microns_project`  
 `$ python manage.py runserver '0.0.0.0:8000'`  

  visit `http://localhost:8080`
