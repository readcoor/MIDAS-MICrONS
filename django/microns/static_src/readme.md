# Static files (CSS, JavaScript, Images)

See the [Django docs](https://docs.djangoproject.com/en/1.9/howto/static-files/)

The `static_src` directory contains static files that will eventually be served by something other than Django (e.g. apache, nginx, or AWS S3).

After modifying this directory, be sure to run this command:

`$ python manage.py collectstatic`  

This will find and copy all static files into ../static, so that beanstalk can serve them.
