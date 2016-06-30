This spins up a Vagrant instance of a Microns development VM.


## Install

1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
1. `$ vagrant init ubuntu/trusty64`
1. `$ vagrant plugin install vagrant-vbguest`
1. `$ vagrant up`
1. `$ vagrant ssh`

## How to

How to save a running vagrant VM as a new template (default name package.box)
$ vagrant package
Make a new directory and mv package.box into it
$ vagrant init package.box
$ vagrant up

## Run django on your local machine

 `$ cd ~/root/dev/microns_project`  
 `$ python manage.py runserver '0.0.0.0:8000'`  

  visit `http://localhost:8080`
