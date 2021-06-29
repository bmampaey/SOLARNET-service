# Production settings - when running under apache web server
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

from project.settings import * # pylint: disable=unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add security settings
# Check with management command "check --deploy"
ALLOWED_HOSTS = ['solarnet.oma.be', 'solarnet2.oma.be']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Logging

# Under apache, the console output is sent to apache log
# so raise the level to WARNING to avoid crowding the apache log with INFO level messages
LOGGING['handlers']['console']['level'] = 'WARNING'

# Send messages level >= INFO to log file
# Send messages level >= WARNING to console (i.e. apache log)
# Send messages level >= ERROR by mail to the admins
LOGGING['root']['handlers'] = ['file', 'console', 'mail_admins']
