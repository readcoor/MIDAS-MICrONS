This spins up a Vagrant instance of a Microns development VM.


## Setup

1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
1. `$ vagrant init ubuntu/trusty64`
1. `$ vagrant plugin install vagrant-vbguest`
1. `$ vagrant up`
1. `$ vagrant ssh`

## How to

How to determine Ubuntu version (default is 14.04)
$ lsb_release -a

How to save a running vagrant VM as a new template (default name package.box)
$ vagrant package
Make a new directory and mv package.box into it
$ vagrant init package.box
$ vagrant up

