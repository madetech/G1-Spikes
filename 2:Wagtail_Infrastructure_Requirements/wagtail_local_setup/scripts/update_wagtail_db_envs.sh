#!/usr/bin/env bash

WAGTAIL_BASE_FILE="app/app/settings/base.py"
WAGTAIL_DEV_FILE="app/app/settings/dev.py"

sed -i -e "/# Database/,+8d" $WAGTAIL_BASE_FILE

echo "
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(\" \")

# Database PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
" > $WAGTAIL_DEV_FILE