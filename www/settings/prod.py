from django.core.exceptions import ImproperlyConfigured

from .common import *


def get_env(name, default=None):
    return os.environ.get(name, default)


def require_env(name):
    value = get_env(name)
    if not value:
        raise ImproperlyConfigured('Missing required environment variable: %s' % name)
    return value

DEBUG = False
ALLOWED_HOSTS = [
    host.strip()
    for host in get_env(
        'DJANGO_ALLOWED_HOSTS',
        'ludovicopratesi.it,www.ludovicopratesi.it,.ludovicopratesi.it,127.0.0.1,localhost',
    ).split(',')
    if host.strip()
]



SECRET_KEY = require_env('DJANGO_SECRET_KEY')

ADMINS = (
    ('Piergiorgio Faraglia', 'p.faraglia@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env('POSTGRES_DB', 'ludovicopratesi_db'),
        'USER': get_env('POSTGRES_USER', 'ludovicopratesi_usr'),
        'PASSWORD': require_env('POSTGRES_PASSWORD'),
        'HOST': get_env('POSTGRES_HOST', '127.0.0.1'),
        'PORT': get_env('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'options': '-c timezone=UTC'
        },
    }
}

WSGI_APPLICATION = 'www.wsgi.application'

CSRF_TRUSTED_ORIGINS = [
    "https://ludovicopratesi.it",
    "https://www.ludovicopratesi.it",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = int(get_env('SECURE_HSTS_SECONDS', '3600'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env('SECURE_HSTS_INCLUDE_SUBDOMAINS', '0') == '1'
SECURE_HSTS_PRELOAD = get_env('SECURE_HSTS_PRELOAD', '0') == '1'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = get_env('SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')
SECURE_CROSS_ORIGIN_OPENER_POLICY = get_env('SECURE_CROSS_ORIGIN_OPENER_POLICY', 'same-origin')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# media settings
MEDIA_ROOT = "/srv/apps/ludovicopratesi/media"
MEDIA_URL = 'https://media.%s/' % DOMAIN_NAME

# static settings
STATIC_ROOT = "/srv/apps/ludovicopratesi/staticfiles"
STATIC_URL = '/static/'

# email settings
EMAIL_HOST = get_env('EMAIL_HOST', 'mail2.mclink.it')
EMAIL_PORT = int(get_env('EMAIL_PORT', '465'))
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', 'info@ludovicopratesi.it')
EMAIL_HOST_PASSWORD = require_env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

GOOGLE_ANALYTICS_MEASUREMENT_ID = get_env('GOOGLE_ANALYTICS_MEASUREMENT_ID', 'G-3R8THL30PZ')

# Logging

PROD_LOG_FILE = '/srv/logs/ludovicopratesi.django.error.log'
PROD_LOG_DIR = os.path.dirname(PROD_LOG_FILE)
PROD_LOG_HANDLER = {
    'level': 'ERROR',
    'class': 'logging.FileHandler' if os.path.isdir(PROD_LOG_DIR) else 'logging.StreamHandler',
}
if os.path.isdir(PROD_LOG_DIR):
    PROD_LOG_HANDLER['filename'] = PROD_LOG_FILE

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': PROD_LOG_HANDLER,
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
