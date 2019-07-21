"""
Django settings for AILab project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from socket import gethostname,gethostbyname

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@j&^@=4t9r&^!@9dq_!_pga=y63#(5oj9tqdk3kvg3r%4ux$d#'

AUTH_TIME_DELTA = 30*60

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'website',
]

MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'AILab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'AILab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR,'testdb.sqlite3'),
        }
    }
}



"""
    'mysqldb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ailabtest',
        'USER': 'ailab',
        'PASSWORD': 'ailab',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
"""
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']   #idont have any idea

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static')
]
STATIC_ROOT = os.path.join(PROJECT_ROOT,'staticRoot')
STATIC_URL = '/static/'

MEDIA_ROOT =  os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

APPEND_SLASH=False

if not os.path.exists('logs'):
    os.makedirs('logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
       #     'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/logs.log',
            'formatter':'standard',
        },  
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['default'],
            'level': 'ERROR',
            'propagate': True
        },
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'website': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },

    }
}

