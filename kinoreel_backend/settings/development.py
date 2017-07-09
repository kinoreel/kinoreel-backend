from .base import *
from .GLOBALS import *
from django.test.runner import DiscoverRunner


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

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelTestRunner, self).teardown_test_environment(**kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False

TEST_RUNNER = 'kinoreel_backend.settings.development.ManagedModelTestRunner'
