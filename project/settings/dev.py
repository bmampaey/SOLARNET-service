# Development settings - when running under django development web server

import os
from project.settings import * # pylint: disable=unused-wildcard-import

# Allow debugging
DEBUG = True

# Allow extra debugging to any ROB client
INTERNAL_IPS = ['127.0.0.1'] + ['192.168.132.'+str(i) for i in range(1, 256)]

# Allow to run on any host
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
	# Add useful management commands
	'django_extensions',
	# Add debug toolbar
	'debug_toolbar',
	# Uncomment to create migrations for tests
	# 'metadata.tests'
]

MIDDLEWARE += [
	# Add debug toolbar
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Use development URLs
ROOT_URLCONF = 'project.urls.dev'

# Change database to development DB
DATABASES['default']['NAME'] = 'dev_solarnet2'
DATABASES['default']['HOST'] = 'localhost'

# Disable password validation
AUTH_PASSWORD_VALIDATORS = []

# Send emails to the console during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging

# Change default formatting of console to match the server format
LOGGING['formatters']['console'] = {
	'format': '[%(asctime)s] %(levelname)s %(message)s',
	'datefmt': '%d/%b/%Y %H:%M:%S',
}

# Send messages level >= INFO to console
LOGGING['root']['handlers'] = ['console']

# LOG SQL queries if environment variable LOG_QUERIES is set
if os.environ.get('LOG_QUERIES', '0') != '0':
	LOGGING['loggers']['django.db.backends'] = {
		'level': 'DEBUG',
	}
