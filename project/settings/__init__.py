# Production settings - when running management command
# See https://docs.djangoproject.com/en/3.2/ref/settings/
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

from pathlib import Path
from django.core.management.utils import get_random_secret_key
from django.utils.log import DEFAULT_LOGGING

SETTINGS_DIR = Path(__file__).resolve().parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = SETTINGS_DIR.parent.parent

# Django Settings
# Debugging
DEBUG = False

# Try to read the secret_key from the file or generate one and write it
SECRET_KEY_FILE = SETTINGS_DIR / 'secret_key.txt'

try:
	with open(SECRET_KEY_FILE, 'rt') as file:
		SECRET_KEY = file.read().strip()
except FileNotFoundError:
	SECRET_KEY = get_random_secret_key()
	with open(SECRET_KEY_FILE, 'wt') as file:
		file.write(SECRET_KEY)

# Don't allow to run on any host (use dev or apache settings to run web server)
ALLOWED_HOSTS = []

# Allow cross domain headers for the RESTful api
# See https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'corsheaders',
	'tastypie',
	'tastypie_swagger',
	'api',
	'dataset',
	'metadata',
	'data_selection'
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'project.utils.middlewares.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'solarnet2',
		'USER': 'solarnet',
		'HOST': 'pgsql-as.oma.be',
		'PORT': '5432',
		'CONN_MAX_AGE': 10 * 60
		# 'PASSWORD': '*****', # Do not put password here, instead write it in the .pgpass file of the user running django
	}
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Specify ISO time format with timezone
DATETIME_FORMAT = 'Y-m-d H:i:s e' # e.g. 1999-12-31 00:00:00 UTC
DATE_FORMAT = 'Y-m-d' # 31 Dec 1999
TIME_FORMAT = 'H:i:s e' # 00:00:00 UTC

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Emails are send in case of server error
ADMINS = [('Benjamin Mampaey', 'benjamin.mampaey@oma.be')]
EMAIL_HOST = 'smtp.oma.be'
SERVER_EMAIL = 'noreply@solarnet2.oma.be'

# Logging

# Use defaults as the basis for our logging setup
LOGGING = DEFAULT_LOGGING

# Redefine the console handler to allow DEBUG level messages
LOGGING['handlers']['console'] = {
	'level': 'DEBUG',
	'class': 'logging.StreamHandler',
	'formatter': 'console'
}

LOGGING['formatters']['console'] = {
	'format': '%(levelname)s %(message)s',
}

# And add an additional log file for INFO level messages
LOGGING['handlers']['file'] = {
	'class': 'logging.handlers.WatchedFileHandler',
	'filename': '/var/log/solarnet_service/django.log',
	'level': 'INFO',
	'formatter': 'file'
}

LOGGING['formatters']['file'] = {
	'format': '[%(asctime)s] %(levelname)s (%(name)s) %(message)s',
}

# Set default logging parameters on the root logger instead of django
LOGGING['loggers'].pop('django')

# Send messages level >= INFO to log file
# Send messages level >= INFO to console
LOGGING['root'] = {
	'handlers': ['console', 'file'],
	'level': 'INFO',
}

# Add special logger for the RequestLoggingMiddleware
LOGGING['formatters']['requests'] = {
	'format': '[%(asctime)s] [%(levelname)s] %(message)s',
}

LOGGING['handlers']['requests'] = {
	'class': 'logging.handlers.WatchedFileHandler',
	'filename': '/var/log/solarnet_service/requests.log',
	'level': 'INFO',
	'formatter': 'requests'
}

LOGGING['loggers']['requests'] = {
	'level' : 'INFO',
	'handlers': ['requests'],
	'propagate': False
}

## Project specific settings

# The characters that should not appear in a data location file_path
FILE_PATH_FORBIDDEN_CHARACTERS = {
	'\\': 'Backslash',
	':': 'Colon',
	'*': 'Asterisk',
	'?': 'QuestionMark',
	'"': 'QuotationMark',
	'\'': 'Apostrophe',
	'<': 'Less-Than Sign',
	'>': 'Greater-Than Sign',
	'|': 'Vertical Line',
	'\r': 'Carriage Return',
	'\n': 'New Line',
	'\0': 'Null',
}

# The maximum size of a ZIP archives generated for a data selection (in bytes)
ZIP_ARCHIVE_MAX_SIZE = 100*1024*1024 # 100 MB

# The maximum size of a file inside a ZIP archives generated for a data selection (in bytes)
ZIP_ARCHIVE_MAX_FILE_SIZE = 100*1024*1024 # 100 MB

# The name of the file in a ZIP archive listing files that could not be included
ZIP_ARCHIVE_MISSING_FILE_NAME = 'missing_files.txt'

# The code to warn the user that the ZIP archive was truncated because it is too large
ZIP_ARCHIVE_TRUNCATED_WARNING = 'Truncated'

# The base URL of the HTTP server
HTTP_BASE_URL = 'https://solarnet.oma.be/'

# The base URL of the FTP server
FTP_BASE_URL = 'ftp://solarnet2.oma.be/data_selection'

# The maximum size of a file that can be downloaded via FTP (in bytes)
FTP_MAX_FILE_SIZE = 100*1024*1024 # 100 MB
