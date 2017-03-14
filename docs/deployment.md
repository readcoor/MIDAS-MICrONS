# Troubleshooting deployments

## How to deploy

```
$ eb deploy <optional:env-name>
```

## Run tests
See master recipe (below) for `manage.py`
```
$ ./manage.py test
.........................
Ran 30 tests in 39.824s
OK (skipped=5)
```

## DISALLOWED_HOST error:
  Most likely this will happen with the dev environment.  
  You might need to specify the hostname ENV variable:  
  `ALLOWED_HOST:  readcoor-env.svt9kqmahy.us-east-1.elasticbeanstalk.com`  
  Use AWS console: use the EB configuration dashboard

## Deploy failed
   Deploy command (`python manage.py migrate`) in `.ebextensions/02_dependencies.config` fails because it's waiting for interactive yes/no  
   Poor solution: don't use `--noinput` because it will answer "no" instead of "yes"  
   Solution: use `yes "yes" | python manage.py migrate`  
   http://stackoverflow.com/questions/35248952/applying-django-migrations-in-a-non-interactive-environment

## Can't login to django after a deployment
  Can't login with oauth to access API  
  Typically happens on dev environment  
  cause: dev environment not white listed by Keycloak/theBoss  
  solution: add dev hostname to keycloak (must ask Dean Kleissas@JHU to add hostname)

## Master recipe for running `manage.py` on AWS Elastic Beanstalk instance
```
local$ eb ssh
 <connected to elastic beanstalk instance>
$ sudo -s
$ source /opt/python/run/venv/bin/activate
$ source /opt/python/current/env
$ cd /opt/python/current/app
$ ./manage.py <command>
```


## Example data is missing
You will need to load example data into the database. 
Use `manage.py` (see above) on the EB instance to run a django shell

```
$ ./manage.py shell
>>> from nada.fixtures import is_empty, nuke_all, boss_setup, neurons_setup
>>> from nada.fixtures import BOSS_CLASSES, NEURONS_CLASSES, NEURONS_DEFAULT_OPTIONS
>>> >>> is_empty(BOSS_CLASSES)
True
>>> is_empty(NEURONS_CLASSES)
True
>>> boss_setup()
>>> neurons_setup(**NEURONS_DEFAULT_OPTIONS)
```
note: `neurons_setup()` will be slow, takes maybe 20 minutes
  

