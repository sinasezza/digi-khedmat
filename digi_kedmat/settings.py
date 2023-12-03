import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key - Debug - Allowed Hosts
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = eval(os.environ.get('DEBUG'))
if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS'))
    

# Authentication Model
AUTH_USER_MODEL = 'account.Account'

# installed Apps for Application
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third party apps
    'rest_framework',
    'bootstrap5',
    'phonenumber_field',
    
    # self apps
    'account',
    
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

ROOT_URLCONF = 'digi_kedmat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'digi_kedmat.wsgi.application'

# Database
DATABASES = {
    'default': eval(os.environ.get('DATABASE_INFO'))
}


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
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
TIME_ZONE = os.environ.get('TIME_ZONE')
USE_I18N = os.environ.get('USE_I18N')
USE_TZ = os.environ.get('USE_TZ')


# Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('STATIC_URL')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]


# Media Files (image, video, ...)
MEDIA_URL = os.environ.get('MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# default Auto Field
DEFAULT_AUTO_FIELD = os.environ.get('DEFAULT_AUTO_FIELD')


# PhoneNumberField Configurations
PHONENUMBER_DEFAULT_REGION = os.environ.get("PHONENUMBER_DEFAULT_REGION")
PHONENUMBER_DEFAULT_FORMAT = os.environ.get("PHONENUMBER_DEFAULT_FORMAT")