from .base import *
from .GLOBALS import *

# SECURITY CONFIG

DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': PG_SERVER,
        'NAME': PG_DB_DEV,
        'USER': PG_USERNAME,
        'PORT': PG_PORT,
        'PASSWORD': PG_PASSWORD,
    }
}
