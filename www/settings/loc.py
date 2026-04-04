from .common import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'db.sqlite3'),
    }
}

# media
MEDIA_ROOT = '/home/xm3ron/src/_media/ludovicopratesi.it/'
MEDIA_URL = '/media/'

# static settings
STATIC_URL = '/static/'

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
