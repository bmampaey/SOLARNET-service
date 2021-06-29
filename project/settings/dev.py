# Development settings

import os
from .base import * # pylint: disable=unused-wildcard-import

### Core Settings
## Debugging
DEBUG = True

## Security
# Allow to run on any host
ALLOWED_HOSTS = ['*']

# Disable password validation
AUTH_PASSWORD_VALIDATORS = []

## Database
# Change database to development DB
DATABASES['default']['NAME'] = 'dev_solarnet2'
DATABASES['default']['HOST'] = 'localhost'


## HTTP
# Allow extra debugging to any ROB client
INTERNAL_IPS = ['127.0.0.1'] + ['192.168.132.'+str(i) for i in range(1, 256)]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware', # Allow cross domain
	*MIDDLEWARE,
	'debug_toolbar.middleware.DebugToolbarMiddleware', # Add debug toolbar
]

ROOT_URLCONF = 'project.urls_dev'

# Cross domain See https://github.com/ottoyiu/django-cors-headers/
# In production this is configured on apache2
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS += [
	# Allow cross domain for the development server
	'corsheaders',
	# Add useful management commands
	'django_extensions',
	# Add debug toolbar
	'debug_toolbar',
	# Uncomment to create migrations for tests
	# 'metadata.tests'
]


### Logging
# Log all database SQL queries to the console
if os.environ.get('LOG_QUERIES', '0') != '0':
	LOGGING['loggers']['django.db.backends'] = {
		'handlers': ['console'],
		'level': 'DEBUG',
	}
