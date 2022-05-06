"""
Django settings for djangoBlog project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l7h#s5lbnicgj88l-r373yi*-u^s1xbevnu)%65o74%6$8g1-f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'blog',
    'parler',
    'crispy_forms',
    'rest_framework',
    'rosetta',
    'django_sass',
    'django_editorjs_fields',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom middlewares
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'djangoBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'djangoBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# custom settings
LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },  # English
        {'code': 'vi', },  # Vietnamese
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LOGIN_URL = "/ua/login"

# All settings common to all environments
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "blog/static",
]

EDITORJS_VERSION = '2.22.3'

EDITORJS_DEFAULT_PLUGINS = (
    'editorjs-paragraph-with-alignment@3.x',
    '@editorjs/image',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/checklist',
    '@editorjs/quote',
    '@editorjs/raw',
    '@editorjs/code',
    '@editorjs/inline-code',
    '@editorjs/embed',
    '@editorjs/delimiter',
    '@editorjs/warning',
    '@editorjs/link',
    '@editorjs/marker',
    '@editorjs/table',
    '@vtchinh/gallery-editorjs@1.1.5', # forked from mr8bit/carousel-editorjs
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'paragraph': {
      'class': 'Paragraph',
      'inlineToolbar': True,
    },
    'Image': {
        'class': 'ImageTool',
        'inlineToolbar': True,
        "config": {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': True,
        'config': {
            'placeholder': 'Enter a header',
            'levels': [2, 3, 4],
            'defaultLevel': 2,
        }
    },
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'List': {'class': 'List', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'InlineCode': {'class': 'InlineCode'},
    'Embed': {'class': 'Embed'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'LinkTool': {
        'class': 'LinkTool',
        'config': {
            'endpoint': reverse_lazy('editorjs_linktool'),
        }
    },
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
    'carousel': {
        'class': 'Carousel',
        'inlineToolbar': True,
        'config': {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
    }
}