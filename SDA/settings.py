"""
Django settings for SDA project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '7h-t62i8qb^farv3hyp%+@3$^vjif!lj_u18+75(!_s35q1h4i'

# To avoid the secret key being sent to github
try:
	from secret_key import *
except ImportError:
	from django.utils.crypto import get_random_string
	import os
	SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))
	secret_key = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
	with open(os.path.join(SETTINGS_DIR, 'secret_key.py'), "w") as f:
		f.write("SECRET_KEY = '%s'\n" % secret_key)
	from secret_key import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'tastypie',
	'wizard',
	'common',
	'dataset',
	'eit',
	'swap',
	'aia_lev1',
	'hmi_magnetogram'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SDA.urls'

WSGI_APPLICATION = 'SDA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'sda',
		'USER': 'postgres',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
	'eit': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'sda',
		'USER': 'eit',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
	'swap': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'sda',
		'USER': 'swap',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
	'aia_lev1': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'sda',
		'USER': 'aia_lev1',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
	'hmi_magnetogram': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'sda',
		'USER': 'hmi_magnetogram',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
}

DATABASE_ROUTERS = ['SDA.database_routers.DataSetRouteur']

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = False

USE_TZ = False

SHORT_DATETIME_FORMAT = DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATE_DIRS = ("SDA/templates/",)

# Login Logout
LOGIN_URL = 'wizard/login'
LOGOUT_URL = 'wizard/logout'

# Mails config
EMAIL_HOST = "smtp.oma.be"
ADMINS = [("Benjamin Mampaey", "benjamin.mampaey@oma.be")]
SERVER_EMAIL = "SOLARNET@" + socket.getfqdn(socket.gethostname())
DEFAULT_FROM_EMAIL = "SOLARNET@oma.be"

