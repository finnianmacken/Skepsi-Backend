"""
Django settings for skepsi_backend project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import dotenv
import django_heroku
import environ


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#
# dotenv_file = os.path.join(BASE_DIR, ".env")
# if os.path.isfile(dotenv_file):
#     dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9@7f=%7!f&af(@vwb9o!hd@h_01-vca*y83u=u7kmxw=fsc8gp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'skepsi_app',
    'graphene_django',
    'corsheaders',
    'rest_framework']


# used for hosting on an actual endpoint rather than localhost (uses ngrok)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'auth0authorization.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'auth0authorization.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': env("JWT_AUDIENCE_VARIABLE"),
    'JWT_ISSUER': 'https://skepsi.us.auth0.com/',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

GRAPHENE = {
    "SCHEMA": "skepsi_app.schemas.schema",
    "MIDDLEWARE": [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TODO: Configure this for our specific domain later
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'skepsi_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'build', ],
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

WSGI_APPLICATION = 'skepsi_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

ALLOWED_HOSTS = ['skepsi-app.herokuapp.com',
                 '127.0.0.1:8000',
                 'localhost',
                 'skepsi-api.herokuapp.com']



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# HEROKU CONFIGURATIONS

import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)

django_heroku.settings(locals())
#
# options = DATABASES['default'].get('OPTIONS', {})
# options.pop('sslmode', None)


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

BROKER_URL = 'amqp://finn:finn@localhost:5672/myvhost'
CELERY_RESULT_BACKEND = 'rpc://'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 86400}
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
