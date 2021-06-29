# Test settings

from .base import * # pylint: disable=unused-wildcard-import

# Run coverage when testings, will only work if the environment variable COVERAGE_PROCESS_START is set to the path of a coverage settings file
try:
	import coverage
except ImportError:
	pass
else:
	coverage.process_startup()

# Allow to run on any host
ALLOWED_HOSTS = ['*']

# Add the test models for metadata
INSTALLED_APPS += ['metadata.tests']

## HTTP

ROOT_URLCONF = 'project.urls_test'
STATICFILES_DIRS = ['dataset/tests/static/']

## Database
# Change database to test DB, set the same name for default and the test DB
# so that when testing the mount_data_selection_filesystem management command
# it can sees the test data that was created during the test
DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['NAME'] = 'test_solarnet2'
DATABASES['default']['TEST'] = {'NAME':  DATABASES['default']['NAME']}
