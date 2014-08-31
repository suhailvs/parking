"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ON_ARVIXE=False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v^qhk(gj==5tlr&%e-76b_#3l*rd#!=x72xnyxcfdeq^lk(%9('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # apps
    "account",
    'bootstrapform',
    'selectize',
    # custom apps
    'homepage',
    'ajaxviews',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATA_DIR=BASE_DIR
if 'OPENSHIFT_DATA_DIR' in os.environ:
    DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# the server time zone, if local use GMT timezone 
TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'homepage','static', 'media')
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request", "account.context_processors.account",
)

# gmail server settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'suhailvs@gmail.com'
EMAIL_HOST_PASSWORD = 'pnaoeogqwtqlgusd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#django-user-accounts
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
USE_TZ=False
if ON_ARVIXE:
    TIME_ZONE = "America/Los_Angeles"
    STATIC_URL="/static/parking/"
    MEDIA_URL = STATIC_URL+'media/'
    USE_TZ =False
    STATIC_ROOT = '/home/suhails/public_html/static/parking'

    # static files are serving automatically so don't need static_root
    #STATIC_ROOT = '/home/suhails/public_html/static/parking'
