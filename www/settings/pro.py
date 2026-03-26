from .common import *

DEBUG = False

ADMINS = (
    ('Piergiorgio Faraglia', 'p.faraglia@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ludovicopratesi_db',
        'USER': 'ludovicopratesi',
        'PASSWORD': 'P"xE:Mar>Vh\g5u3',
    }
}

ALLOWED_HOSTS = ["."+DOMAIN_NAME]
WSGI_APPLICATION = 'www.wsgi.application'

# media settings
MEDIA_ROOT = '/home/ludovicopratesi/media/'
MEDIA_URL = 'https://media.%s/' % DOMAIN_NAME

# static settings
STATIC_ROOT = '/home/ludovicopratesi/static/'
STATIC_URL = '/static/'

# email settings
EMAIL_HOST = 'mail2.mclink.it'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'info@ludovicopratesi.it'
EMAIL_HOST_PASSWORD = 'LudPra1'
EMAIL_USE_SSL = True

# django_compressor
COMPRESS_OFFLINE = True

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/ludovicopratesi/var/log/django.error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
