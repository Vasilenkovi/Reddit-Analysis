"""
Django settings for DjangoRed project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from os import environ
from omegaconf import OmegaConf
BASE_DIR = Path(__file__).resolve().parent.parent
# SECRET_KEY = environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-ecwm#*8s14myek8xi+%yc1tk$v2@=&l18=cg8(a+rk7rrz+k@f'

# DEBUG = int(environ.get('DEBUG', default=0))

# ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(' ')
# Build paths inside the project like this: BASE_DIR / 'subdir'.

DJANGO_SUPERUSER_PASSWORD="Vasilenich"
DJANGO_SUPERUSER_USERNAME="Vasilenich"
DJANGO_SUPERUSER_EMAIL="my_user@domain.com"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-4bfml7%ip4g#@3^5mfrq486wsraeww*9=mq$qnt^ig2irb*^u$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '51.250.112.4', '0.0.0.0', 'backendserv']

# Application definition

INSTALLED_APPS = [
    'daphne',
    #'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'bootstrap5',
    'HomeApp',
    'VisualizationApp',
    'ParserApp',
    'DatasetViewApp',
    'AccountsApp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoRed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'DjangoRed.wsgi.application'
ASGI_APPLICATION = 'DjangoRed.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reddit_test_accounts',
        'USER': 'test_accounts_client',
        'PASSWORD': 't9a!4Ic1G+X',
        'HOST': 'mysqlred',
        'PORT': '3306',
    },
}

NATIVE_SQL_DATABASES = {
    'job_id': OmegaConf.load(BASE_DIR / "DjangoRed/config/MySQL_local_jobid.yaml"),

    'parser': OmegaConf.load(BASE_DIR / "DjangoRed/config/MySQL_local_parser.yaml"),

    'dataset_reader': OmegaConf.load(BASE_DIR / "DjangoRed/config/MySQL_local_parser_reader.yaml"),

    'clustering_read': OmegaConf.load(BASE_DIR / "DjangoRed/config/MySQL_local_clustering_reader.yaml"),

    'clustering_saving': OmegaConf.load(BASE_DIR / "DjangoRed/config/MySQL_local_clustering_saving.yaml"),
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = "/statics"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CHANNELS_LAYERS = {
#   'default': {
#     'BACKEND': 'channels.layers.InMemoryChannelLayer'
#   }
# }

# Parser config
REDDIT_CLIENT = OmegaConf.load(BASE_DIR / "DjangoRed/config/reddit_script_config.yaml")

#CELERY
CELERY_IMPORTS = ("ParserApp.tasks")
CELERY_BROKER_URL = 'amqp://guest:guest@message-broker:5672//'
# Session

SESSION_DATASET_IDS = "dataset_ids"

SECURE_CROSS_ORIGIN_OPENER_POLICY=None

AUTH_USER_MODEL = "AccountsApp.UserAccount"

LOGIN_REDIRECT_URL = 'HomeApp:home'
LOGIN_URL = 'HomeApp:home'
LOGOUT_URL = 'HomeApp:home'