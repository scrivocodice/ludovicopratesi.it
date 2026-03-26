from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ludovicopratesi_db',
        'USER': 'xm3ron',
        'PASSWORD': 'thesis',
    }
}

# media
MEDIA_ROOT = '/home/xm3ron/src/_media/ludovicopratesi.it/'
MEDIA_URL = '/media/'

# static settings
STATIC_URL = '/static/'
COMPRESS_ROOT = '/tmp/'

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
