"""
Django settings for the microns project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    SECRET_KEY = '<secret key>'

# SECURITY WARNING: don't run with debug turned on in production!
if 'DEBUG' in os.environ:
    DEBUG = os.environ['DEBUG'].upper() == 'TRUE'  # turn off when we actually go into production
else:
    DEBUG = True

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'nada',
    'rest_framework',
    'rest_framework_swagger',
    'bossoidc',
    'djangooidc'
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'bossoidc.backend.OpenIdConnectBackend'
    ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    # ...
    'rest_framework.authentication.SessionAuthentication',
    'oidc_auth.authentication.BearerTokenAuthentication',
    )
    }

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'microns.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['microns/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'microns.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

SQLITE_DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Use sqlite on dev machine. Use postgres for production
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'microns',
        'USER': 'tester',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': ''
    }}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')
STATIC_URL = '/static/'

API_VERSION = 'v1'

THEBOSS_CONFIG = os.path.join(BASE_DIR, 'theboss.cfg')

LOGOUT_URL = 'https://api.theboss.io/openid/logout'

auth_uri = "https://auth.theboss.io/auth/realms/BOSS"
client_id = "church" # Client ID configured in the Auth Server

# public_uri: the address that the client will be redirected back to
# NOTE: the public uri needs to be configured in the Auth Server
#       as a valid uri to redirect to
if 'IS_PRODUCTION' in os.environ:
    public_uri = 'https://%s' % os.environ['ALLOWED_HOST']
else:
    public_uri = "http://localhost:8080/docs" 

from bossoidc.settings import *
configure_oidc(auth_uri, client_id, public_uri)

