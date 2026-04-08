from .common import *

# DEBUG = False
# ALLOWED_HOSTS = [
#     "ludovicopratesi.it",
#     "www.ludovicopratesi.it",
#     ".ludovicopratesi.it",
#     "127.0.0.1",
#     "localhost",
# ]
DEBUG = True
ALLOWED_HOSTS = ["*"]


ADMINS = (
    ('Piergiorgio Faraglia', 'p.faraglia@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ludovicopratesi_db',
        'USER': 'ludovicopratesi_usr',
        'PASSWORD': 'Unmarked7-Pampers0-Banked4-Estimator1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
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
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# media settings
MEDIA_ROOT = "/srv/apps/ludovicopratesi/media"
MEDIA_URL = 'https://media.%s/' % DOMAIN_NAME

# static settings
STATIC_ROOT = "/srv/apps/ludovicopratesi/staticfiles"
STATIC_URL = '/static/'

# email settings
EMAIL_HOST = 'mail2.mclink.it'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@ludovicopratesi.it'
EMAIL_HOST_PASSWORD = 'LudPra1'
EMAIL_USE_SSL = True

GOOGLE_ANALYTICS_MEASUREMENT_ID = 'G-3R8THL30PZ'

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
