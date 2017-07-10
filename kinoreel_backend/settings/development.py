from .base import *
from django.test.runner import DiscoverRunner

try:
    from .GLOBALS import *
except ImportError or ModuleNotFoundError:
    PG_SERVER = os.environ['PG_SERVER']
    PG_PORT = os.environ['PG_PORT']
    PG_DB = os.environ['PG_DB']
    PG_USERNAME = os.environ['PG_USERNAME']
    PG_PASSWORD = os.environ['PG_PASSWORD']

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': PG_SERVER,
        'NAME': 'test_{}_dev'.format(PG_DB),
        'USER': PG_USERNAME,
        'PORT': PG_PORT,
        'PASSWORD': PG_PASSWORD,
    }
}


class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    """
    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        self.unmanaged_models = [m for m in apps.get_models()
                                 if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(ManagedModelTestRunner, self).setup_test_environment(**kwargs)

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelTestRunner, self).teardown_test_environment(**kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False

TEST_RUNNER = 'kinoreel_backend.settings.development.ManagedModelTestRunner'
