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
DEBUG = False

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'mysite','templates')]

ALLOWED_HOSTS = [
    '.flexspot.webfactional.com',
    '.flexlot.co',
   # '127.0.0.1', 'localhost'
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
    'captcha',
    #kombu.transport.django',
    'djcelery',
    # custom apps
    
    'payments',    
    'ajaxviews',
    'customemails',
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
    'homepage.custom_middleware.RestrictAdminMiddleware',
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

USE_TZ = False

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request", "account.context_processors.account",
)
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS+(
    "account.auth_backends.EmailAuthenticationBackend",
)

# gmail server settings

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'flexspot'
EMAIL_HOST_PASSWORD = 'Password123'#'pnaoeogqwtqlgusd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'support@www.flexlot.co'
"""
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'info@flexspot.co'
EMAIL_HOST_PASSWORD = 'Password123'
EMAIL_PORT = 80
EMAIL_USE_TLS = False
"""

DEFAULT_FROM_EMAIL = 'support@flexspot.co'
CONTACT_US_EMAIL='info@flexspot.co' #'suhailvs@gmail.com'

#django-user-accounts
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

#DJango recaptcha(https://www.google.com/recaptcha/admin)
RECAPTCHA_PUBLIC_KEY = '6LfgU_oSAAAAAABjYNwiprQV-9BO9yH7C9pkGDkt'
RECAPTCHA_PRIVATE_KEY = '6LfgU_oSAAAAAORVMk6HGflbZx0rbShkn2sNjlXY'
RECAPTCHA_USE_SSL = False



import djcelery
djcelery.setup_loader()
#BROKER_URL = 'django://'
BROKER_URL = 'sqla+mysql://flexspot_user:Flexspot123@localhost/celerytasks'

"""
 1) master  --> flexlot.co
 2) develop --> dev.flexlot.co
 3) local   --> localhost:8000
"""
site_branch='develop' #master, develop, local
if site_branch == 'master':
    STATIC_URL = 'http://static.flexspot.webfactional.com/flexspot/'
    MEDIA_URL = STATIC_URL+'media/'
    STATIC_ROOT='/home/flexspot/webapps/htdocs/flexspot/'
    MEDIA_ROOT = os.path.join(STATIC_ROOT,'media')
    TIME_ZONE = 'US/Eastern'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'flexspotdb',
            'USER': 'flexspot_user',
            'PASSWORD': 'Flexspot123',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }

    # live paypal settings
    PAYPAL_RECEIVER_EMAIL = "info@flexspot.co"
    PAYPAL_REDIRECT_URL = "http://www.flexspot.co"
    PAYPAL_TEST = False

elif site_branch == 'develop':
    STATIC_URL = 'http://static.flexspot.webfactional.com/flexspot_dev/'
    MEDIA_URL = STATIC_URL+'media/'
    STATIC_ROOT='/home/flexspot/webapps/htdocs/flexspot_dev/'
    MEDIA_ROOT = os.path.join(STATIC_ROOT,'media')
    TIME_ZONE = 'US/Eastern'

    #for paypal testing
    # please use --> email: parkingbuyer@testing.com, password: suhail412  
    PAYPAL_RECEIVER_EMAIL = "info-facilitator@flexspot.co"
    PAYPAL_REDIRECT_URL = "http://dev.flexlot.co"
    PAYPAL_TEST = True


else:
    TEMPLATE_DEBUG = DEBUG =True
    ALLOWED_HOSTS += ['127.0.0.1','localhost'] # please addthis for template_debug false

    STATIC_URL = '/static/'
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR,'homepage','static', 'media')    

    PAYPAL_RECEIVER_EMAIL = "info-facilitator@flexspot.co"
    PAYPAL_REDIRECT_URL = "http://localhost:8000"
    PAYPAL_TEST = True

    ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
