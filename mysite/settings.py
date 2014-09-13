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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v^qhk(gj==5tlr&%e-76b_#3l*rd#!=x72xnyxcfdeq^lk(%9('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'mysite','templates')]

ALLOWED_HOSTS = [
    '.flexspot.co',
    '.flexspot.webfactional.com',
    '.flexlot.co',
]


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
    'homepage',
    "account",
    'bootstrapform',
    'selectize',
    'paypal.standard.ipn',
    # custom apps
    
    'payments',    
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
AUTH_USER_MODEL = 'ajaxviews.MyUser'
ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

on_webfaction=False
if on_webfaction:
    STATIC_URL = 'http://static.flexspot.webfactional.com/flexspot_dev/'
    MEDIA_URL = STATIC_URL+'media/'
    STATIC_ROOT='/home/flexspot/webapps/htdocs/flexspot_dev/'
    MEDIA_ROOT = os.path.join(STATIC_ROOT,'media')
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR,'homepage','static', 'media')

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request", "account.context_processors.account",
)

# gmail server settings
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'flexspot'
EMAIL_HOST_PASSWORD = 'Password123'#'pnaoeogqwtqlgusd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'support@flexspot.co'
SERVER_EMAIL = 'support@www.flexlot.co'
#django-user-accounts
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True



PAYPAL_RECEIVER_EMAIL = "info-facilitator@flexspot.co"
PAYPAL_REDIRECT_URL = "http://dev.flexlot.co"
PAYPAL_TEST = True
