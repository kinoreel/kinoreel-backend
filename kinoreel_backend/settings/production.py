from .base import *


# SECURITY CONFIG

DEBUG = True

HOST = os.environ.get("ALLOWED_HOST", "0.0.0.0")
print("ALLOWED_HOST is %s", HOST)
ALLOWED_HOSTS = ["0.0.0.0", "api.unruffled-nightingale.com"]

try:
    from .GLOBALS import *
except ImportError or ModuleNotFoundError:
    PG_SERVER = os.environ['PG_SERVER']
    PG_PORT = os.environ['PG_PORT']
    PG_DB = os.environ['PG_DB']
    PG_USERNAME = os.environ['PG_USERNAME']
    PG_PASSWORD = os.environ['PG_PASSWORD']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': PG_SERVER,
        'NAME': PG_DB,
        'USER': PG_USERNAME,
        'PORT': PG_PORT,
        'PASSWORD': PG_PASSWORD,
    }
}
