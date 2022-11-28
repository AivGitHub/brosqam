"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import io
import os
from pathlib import Path

import environ
from google.cloud import secretmanager


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# [Custom]
PROJECT_NAME = 'brosqam'

ENV_FILE_NAME = os.environ.get('BQ_ENV_NAME', '.env')
ENV_FILE_PATH = os.path.join(BASE_DIR, ENV_FILE_NAME)
GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')
TRAMPOLINE_CI = os.environ.get('TRAMPOLINE_CI')

ENV = environ.Env()

# TODO: think about that, secrets should be got from the secrets managers and environ from environ
if os.path.isfile(ENV_FILE_PATH) and not GOOGLE_CLOUD_PROJECT and not TRAMPOLINE_CI:
    # Local environ from .env
    ENV.read_env(ENV_FILE_PATH)
elif GOOGLE_CLOUD_PROJECT and not TRAMPOLINE_CI:
    # Google secret manager environ
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    settings_name = os.environ.get('SETTINGS_NAME', 'django_settings')

    client = secretmanager.SecretManagerServiceClient()
    name = 'projects/%s/secrets/%s/versions/latest' % (project_id, settings_name)
    payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')

    ENV.read_env(io.StringIO(payload))
elif TRAMPOLINE_CI and not GOOGLE_CLOUD_PROJECT:
    # CI environ
    placeholder = (
        f'BQ_SECRET_KEY=a\n'
        'GS_BUCKET_NAME=None\n'
        'BQ_ALLOWED_HOSTS=*\n'
        'BQ_DEBUG=True\n'
    )
    ENV.read_env(io.StringIO(placeholder))
else:
    raise RuntimeError('No or more than one virtual environment provided')
# [/Custom]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get_value('BQ_SECRET_KEY')


# By default, always run in production mode
DEBUG = ENV.get_value('BQ_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ENV.get_value('BQ_ALLOWED_HOSTS', cast=list)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
if not TRAMPOLINE_CI:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': PROJECT_NAME,
            'USER': PROJECT_NAME,
            'PASSWORD': ENV.get_value('BQ_PSQL_PASSWORD'),
            'HOST': ENV.get_value('BQ_PSQL_HOST'),
            'PORT': ENV.get_value('BQ_PSQL_PORT', default='5432'),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': PROJECT_NAME,
        },
    }


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = str(BASE_DIR / 'static/')

MEDIA_URL = 'media/'
MEDIA_ROOT = str(BASE_DIR / 'media/')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'