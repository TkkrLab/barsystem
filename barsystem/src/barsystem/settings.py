"""
DO NOT CHANGE THIS FILE!

CHANGES SHOULD BE MADE IN local_settings.py!!!
"""
import os


def gettext_noop(s):
    return s


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.expanduser('~/.config/barsystem')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_FILE = os.path.join(CONFIG_DIR, 'secret.txt')
if os.path.exists(SECRET_KEY_FILE):
    SECRET_KEY = open(SECRET_KEY_FILE).read()
else:
    SECRET_KEY = 'TERRIBLE'
    import warnings
    class BadlyConfiguredWarning(Warning):
        pass
    warnings.warn(
        'The default secret key is terrible! Run barsystem-installer!',
        BadlyConfiguredWarning
    )

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'barsystem',
    'barsystem.gui'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CONFIG_DIR, 'barsystem.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('nl', gettext_noop('Dutch')),
    ('en', gettext_noop('English')),
    # ('de', gettext_noop('German')),
]

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Root URL and WSGI
ROOT_URLCONF = 'barsystem.urls'
WSGI_APPLICATION = 'barsystem.wsgi.application'

# Config for django.contrib.messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Settings to improve security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
