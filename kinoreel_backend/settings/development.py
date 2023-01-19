from .base import *
from unittest import defaultTestLoader  # noqa
from django.test.utils import setup_test_environment, teardown_test_environment
from django.conf import settings
from django.test import TestCase
from importlib import import_module
import xmlrunner

from django.test.runner import DiscoverRunner, reorder_suite

try:
    from .GLOBALS import *
except ImportError or ModuleNotFoundError:
    PG_SERVER = os.environ['PG_SERVER']
    PG_PORT = os.environ['PG_PORT']
    PG_DB = os.environ['PG_DB']
    PG_USERNAME = os.environ['PG_USERNAME']
    PG_PASSWORD = os.environ['PG_PASSWORD']

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0"]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': PG_SERVER,
        'NAME': '{}'.format(PG_DB),
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

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = None
        root = getattr(settings, 'TEST_DISCOVER_ROOT', '.')
        top_level = getattr(settings, 'TEST_DISCOVER_TOP_LEVEL', None)
        pattern = getattr(settings, 'TEST_DISCOVER_PATTERN', 'test*.py')

        if test_labels:
            suite = defaultTestLoader.loadTestsFromNames(test_labels)
            # if single named module has no tests, do discovery within it
            if not suite.countTestCases() and len(test_labels) == 1:
                suite = None
                root = import_module(test_labels[0]).__path__[0]

        if suite is None:
            suite = defaultTestLoader.discover(root,
                                               pattern=pattern, top_level_dir=top_level)

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.
        Labels must be of the form:
         - app.TestClass.test_method
        Run a single specific test method
         - app.TestClass
        Run all the test methods in a given class
         - app
        Search for doctests and unittests in the named application.

        When looking for tests, the test runner will look in the models and
        tests modules for the application.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        setup_test_environment()

        settings.DEBUG = False

        verbosity = getattr(settings, 'TEST_OUTPUT_VERBOSE', 1)
        if isinstance(verbosity, bool):
            verbosity = (1, 2)[verbosity]
        descriptions = getattr(settings, 'TEST_OUTPUT_DESCRIPTIONS', False)
        output = getattr(settings, 'TEST_OUTPUT_DIR', '.')

        suite = self.build_suite(test_labels, extra_tests)

        old_config = self.setup_databases()

        result = xmlrunner.XMLTestRunner(
            verbosity=verbosity, descriptions=descriptions,
            output=output).run(suite)

        self.teardown_databases(old_config)
        teardown_test_environment()

        return len(result.failures) + len(result.errors)

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelTestRunner, self).teardown_test_environment(**kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False


TEST_RUNNER = 'kinoreel_backend.settings.development.ManagedModelTestRunner'
