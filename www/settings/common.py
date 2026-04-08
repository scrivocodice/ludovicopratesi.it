import os
import sys

DOMAIN_NAME = 'ludovicopratesi.it'

SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, '..', '..'))
APP_PATH = os.path.join(PROJECT_PATH, 'app')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')

if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

LANGUAGE_CODE = 'it'
LANGUAGES = (
    ('it', 'italiano'),
)
USE_I18N = True

TIME_ZONE = 'Europe/Rome'
USE_TZ = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local-development-only-secret-key')

LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, 'locale'),
]

STATICFILES_DIRS = [
    SRC_PATH,
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'www.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'easy_thumbnails',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

THUMBNAIL_PROCESSORS = [
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
]

THUMBNAIL_ALIASES = {
    '': {
        'window': {'size': (233, 220), 'quality': 50, 'crop': True, 'smart': True, 'upscale': True},
        'list': {'size': (291, 218), 'quality': 50, 'crop': True, 'smart': True, 'upscale': True},
        'show': {'size': (637, 388), 'quality': 50, 'crop': True, 'smart': True, 'upscale': True},
    },
}
THUMBNAIL_BASEDIR = 'thumbs'

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

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

GOOGLE_ANALYTICS_MEASUREMENT_ID = ''
