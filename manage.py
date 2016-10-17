#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os, sys
sys.dont_write_bytecode = True

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTTESTTESTTESTTESTTESTTESTTEST')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,testserver').split(',')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
try:
    from django.conf import settings
    from django.shortcuts import render
except ImportError:
    sys.stderr.write("pip install Django>=1.8 to continue...\n")
    sys.exit(1)
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',  # better runserver
    ),
    DATABASES={
        'default': {},
    },
    STATIC_ROOT=os.path.join(BASE_DIR, '__static__'),
    MEDIA_ROOT=os.path.join(BASE_DIR, '__uploads__'),
    STATIC_URL='/__static__/',
    MEDIA_URL='/__uploads__/',
    MESSAGE_STORAGE='django.contrib.messages.storage.cookie.CookieStorage',
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    }],
    SECURE_BROWSER_XSS_FILTER=True,
    SECURE_CONTENT_TYPE_NOSNIFF=True,
)

def generate_card():
    card = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    return card


def single(request):
    card = generate_card()
    context = {'cards': [card]}
    return render(request, 'single.html', context)

def lazy_urls():
    # We make this lazy so that we can import stuff as necessary
    # slightly later than first-execution, which would cause issues
    # due to not having finished bootstrapping.
    from django.conf.urls import url, include
    from django.contrib import admin
    urlpatterns = [
        url(regex='^$', view=single, name='single'),
    ]
    return urlpatterns
from django.utils.functional import SimpleLazyObject
# lazy() will get called N times, SLO will be called once.
# Note: if using django-debug-toolbar, you'd need to manual configure it
# because there's no __radd__ on SLO, see: https://code.djangoproject.com/ticket/26287
urlpatterns = SimpleLazyObject(lazy_urls)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

