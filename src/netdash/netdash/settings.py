"""
Django settings for NetDash project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from os import getenv

import dj_database_url


def csv_to_list(csv, delim=','):
    try:
        return [x.strip() for x in csv.split(delim)]
    except Exception:
        return []


def str_to_bool(val):
    return val.lower() in ('yes', 'true', 'on', '1')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('NETDASH_SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(getenv('NETDASH_DEBUG', 'off'))

ALLOWED_HOSTS = csv_to_list(getenv('NETDASH_ALLOWED_HOSTS', None))

CORS_ORIGIN_ALLOW_ALL = str_to_bool(
    getenv('NETDASH_CORS_ORIGIN_ALLOW_ALL', 'off')
    )

CORS_ORIGIN_WHITELIST = getenv('NETDASH_CORS_ORIGIN_WHITELIST', [])

NETDASH_DEVICE_MODULE = getenv('NETDASH_DEVICE_MODULE',
                               'netdash_device_dummy')

# Required if using the netdash_device_netbox_api module for devices
NETBOX_API_URL = getenv('NETDASH_NETBOX_API_URL', None)

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_swagger',
    'netdash_api',
    'netdash_device_snmp',
    'netdash_device_dummy',
    'netdash_device_netbox_api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'netdash.urls'

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

WSGI_APPLICATION = 'netdash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = getenv('NETDASH_TIME_ZONE', 'America/Detroit')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
