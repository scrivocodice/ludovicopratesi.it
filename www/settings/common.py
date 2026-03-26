import django.conf.global_settings as DEFAULT_SETTINGS
import os, sys

DOMAIN_NAME = 'ludovicopratesi.it'

# ==========================
# = Directory Declarations =
# ==========================
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../'
APP_PATH = os.path.join(PROJECT_PATH, 'app')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
TPL_PATH = os.path.join(PROJECT_PATH, 'tpl')

# =============
# = Classpath =
# =============
sys.path.append(APP_PATH)

SITE_ID = 1

# ------------------
# language settings
# ------------------

# default language
LANGUAGE_CODE = 'it'

# supported languages
LANGUAGES = (
    ('it', 'italiano'),
    ('en', 'english'),
)
USE_I18N = True
#SOLID_I18N_USE_REDIRECTS = False

# timezone settigs
TIME_ZONE = 'Europe/Rome'
USE_TZ = False
USE_L10N = True

SECRET_KEY = 'tl0$hg*+m)a*!nb3#cpau@z!es2c7visyibnx&9j_a382pnidf'

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale"),
)

STATICFILES_DIRS = (
    SRC_PATH,
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'www.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'frontend',
    'easy_thumbnails',
    'mail_templated',
    'compressor',
    'analytical',
    'tinymce',
    'easy_pdf',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# paginator
ITEMS_PER_PAGE = 10

# Easy Thumbnail
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
)

THUMBNAIL_ALIASES = {
    '': {
        'window': {'size':(233, 220),'quality': 50, 'crop': True, 'smart': True, 'upscale':True},
        'list': {'size':(291, 218),'quality': 50, 'crop': True, 'smart': True, 'upscale':True},
        'show': {'size':(637, 388), 'quality': 50, 'crop': True, 'smart': True, 'upscale':True},
    },
}
THUMBNAIL_BASEDIR = "thumbs"

# email settings
EMAIL_CONTACT_ADDRESS = 'lpratesi@futuronline.it'
EMAIL_USE_SSL = True

# analytics
ANALYTICAL_INTERNAL_IPS = ['127.0.0.1','localhost',]
# GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-47054548-1'
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = 'G-3R8THL30PZ'
# GOOGLE_ANALYTICS_JS_PROPERTY_ID = 'G-3R8THL30PZ'
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True
GOOGLE_ANALYTICS_SITE_SPEED = True

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


# TinyMCE settings
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    }

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
