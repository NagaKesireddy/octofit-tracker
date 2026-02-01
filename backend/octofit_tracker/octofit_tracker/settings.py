"""
Django settings for octofit_tracker project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
if os.environ.get('CODESPACE_NAME'):
    ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'workouts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'octofit_tracker.urls'

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

WSGI_APPLICATION = 'octofit_tracker.wsgi.application'

# Database - MongoDB via Djongo
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'octofit_db',
        'ENFORCE_SCHEMA_VALIDATION': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        }
    }
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

# Static files
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Allow credentials (cookies) for development when using session auth from the frontend
CORS_ALLOW_CREDENTIALS = True

if os.environ.get('CODESPACE_NAME'):
    CORS_ALLOWED_ORIGINS.append(f"https://{os.environ.get('CODESPACE_NAME')}-3000.app.github.dev")

# CSRF trusted origins for development (localhost and Codespaces forwarded hosts)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "https://localhost:8000",
]

codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    host_3000 = f"https://{codespace_name}-3000.app.github.dev"
    host_8000 = f"https://{codespace_name}-8000.app.github.dev"
    CORS_ALLOWED_ORIGINS.append(host_3000)
    CORS_ALLOWED_ORIGINS.append(host_8000)
    CSRF_TRUSTED_ORIGINS.extend([host_3000, host_8000])

# Redirect after login/logout
LOGIN_REDIRECT_URL = '/api/workouts/'
LOGOUT_REDIRECT_URL = '/'

# If frontend URL is available (local dev or Codespace), redirect login to frontend UI
FRONTEND_HOST = os.environ.get('FRONTEND_HOST')
if not FRONTEND_HOST:
    if os.environ.get('CODESPACE_NAME'):
        FRONTEND_HOST = f"https://{os.environ.get('CODESPACE_NAME')}-3000.app.github.dev"
    else:
        FRONTEND_HOST = 'http://localhost:3000'

# Prefer full frontend URL for post-login redirect to bring users back to the React UI
LOGIN_REDIRECT_URL = FRONTEND_HOST
LOGOUT_REDIRECT_URL = FRONTEND_HOST
