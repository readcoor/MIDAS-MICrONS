# About this directory

These files initialize the EC2 instance created by Elastic Beanstalk. The files are loaded in alphabetical order.

`01_dependencies.config` loads the following
  1. `epel-release` : this is needed to load postgres libraries that rely on epel
  2. `libffi-devel` : this is needed by the python `cffi` library
  3. Upgrades `pip` from version 6 to version 9
  4. Enable `epel`


