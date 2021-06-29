# Production settings
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

from .base import * # pylint: disable=unused-wildcard-import

### Core Settings
## Debugging
DEBUG = False

## Emails
# Emails are send in case of server error
ADMINS = [('Benjamin Mampaey', 'benjamin.mampaey@oma.be')]
EMAIL_HOST = 'smtp.oma.be'
SERVER_EMAIL = 'noreply@solarnet.oma.be'

## Security
# Allow to run on any host
ALLOWED_HOSTS = ['solarnet.oma.be', 'solarnet2.oma.be']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
