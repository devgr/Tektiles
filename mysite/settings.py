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
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
STATIC_PATH = os.path.join(PROJECT_PATH,'static')
MEDIA_ROOT = os.path.join(PROJECT_PATH,'media')
MEDIA_URL = '/media/'
LOGIN_URL = '/user/login'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '451+6vvt*b0fd2qw8*n_z%g9_97d-^12#q+ck4g!k8_fg-gjr!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']

from django.db import connections
#DATABASE_APPS_MAPPING = {'login': 'default', 'blog': 'blog'}
#DATABASE_ROUTERS = ['blog.routers.Router']

#crispy forms 
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#Email Settings for account activation
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hwtechnicalsolutions@gmail.com'  #Do Not Store On GitHub!!!
EMAIL_HOST_PASSWORD = 'softwareproject'  #No, not this, either.
EMAIL_PORT = 587
EMAIL_USE_TLS = True



# endless pagination
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS 
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)

#search engine 
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor' 


#embedd video
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'companion',
    'blog',
    'webstore',
    'frontend',
    'user_management',
    'crispy_forms',
    #'south',
    'endless_pagination',
    'haystack',
    'imagekit',
    'embed_video',
    'annoying',
)
#User Profile Settings
AUTH_PROFILE_MODULE = "user_management.UserProfile"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'userdb.sqlite3'),
 #       'USER': 'admin',
 #       'PASSWORD': 'password'
    },
    'blog': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'blogdb.sqlite3'),
#        'USER': 'admin',
#        'PASSWORD': 'password'
    },
   'webstore': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'webstoredb.sqlite3'),
#        'USER': 'admin',
#        'PASSWORD': 'password'
    },
    'companion': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'companiondb.sqlite3'),
#        'USER': 'admin',
#        'PASSWORD': 'password'
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'CacheTable',
    }
}

#templete absolute path def
TEMPLATE_DIRS = (

    TEMPLATE_PATH,
)

#static absolute path def
STATICFILES_DIRS = (
    STATIC_PATH,
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'





