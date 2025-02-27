"""
Django settings for event_ticketing_system project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# ============================ENV VARIABLES=====================================
SECRET_KEY = 'django-insecure-u$$_8#ex@r&)_d=b%*zm8zeasd_))@_!ia_uwiz7j_)267kex_'
DEBUG = True
ALLOWED_HOSTS = []

PAGE_SIZE = 10

PROJECT_NAME = 'event_ticketing_system'

DEFAULT_POSTGRES_DATABASE_NAME = "event_ticketing_db"
DEFAULT_POSTGRES_USER = "event_user"
DEFAULT_POSTGRES_PASSWORD = "event_password"
DEFAULT_POSTGRES_HOST = "127.0.0.1"  # 'postgres' inside Docker
DEFAULT_POSTGRES_PORT = "5433"
# ===============================================================================

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'tickets'
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

ROOT_URLCONF = 'event_ticketing_system.urls'

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

WSGI_APPLICATION = 'event_ticketing_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', DEFAULT_POSTGRES_DATABASE_NAME),
        'USER': os.getenv('DATABASE_USER', DEFAULT_POSTGRES_USER),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', DEFAULT_POSTGRES_PASSWORD),
        'HOST': os.getenv('DATABASE_HOST', DEFAULT_POSTGRES_HOST),
        'PORT': os.getenv('DATABASE_PORT', DEFAULT_POSTGRES_PORT),
    }
}



# import dj_database_url
# DATABASE_URL = "postgres://postgres:postgresKesar302@178.16.137.37/arpansahu_one_postgres?currentSchema=ticketing_event_system"
# # DATABASES['default'] =  dj_database_url.config()
# # updated
# DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Required for drf-spectacular
    'COERCE_DECIMAL_TO_STRING': False,  # Ensures DecimalField is serialized as a float
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # Optional, for pagination
    'PAGE_SIZE': PAGE_SIZE  # Optional, sets default page size for list views
}
