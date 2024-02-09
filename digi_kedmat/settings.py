import os
from pathlib import Path
from shutil import which
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#### Secret Key - Debug - Allowed Hosts
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = eval(os.environ.get('DEBUG'))

ALLOWED_HOSTS = eval(os.environ.get("ALLOWED_HOSTS"))
INTERNAL_IPS = eval(os.environ.get("INTERNAL_IPS"))


#### CORS/CSRF Options And Settings
CORS_ALLOWED_ORIGINS = eval(os.environ.get("CORS_ALLOWED_ORIGINS"))
CSRF_TRUSTED_ORIGINS = eval(os.environ.get("CSRF_TRUSTED_ORIGINS"))
CORS_ORIGIN_ALLOW_ALL = eval(os.environ.get("CORS_ORIGIN_ALLOW_ALL"))
CORS_ALLOW_HEADERS = eval(os.environ.get("CORS_ALLOW_HEADERS"))

#### SSL SETTINGS
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True



# Authentication Model
AUTH_USER_MODEL = 'accounts.Account'

# installed Apps for Application
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.forms',

    
    # third party apps
    'rest_framework',
    'corsheaders',
    'phonenumber_field',
    'compressor',
    'cssmin',
    'jsmin',
    'ckeditor',  
    'ckeditor_uploader', 
    'import_export',
    'captcha',
    'django_jalali',
    'jalali_date',
    'tailwind',
    'theme',
    'django_browser_reload',
    # 'debug_toolbar',
    'channels',
    'watchman',
    
    
    # self apps
    'accounts',
    'ads',
    'barters',
    'chat',
    'generics',
    'jobs',
    
]

#### SITE ID
SITE_ID = eval(os.environ.get('SITE_ID'))


MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Serve static in production without nginx or apache
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
        'DIRS': [BASE_DIR / 'templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
            "builtins": [
                "generics.templatetags.generics_tags",
                "generics.templatetags.generics_filters",
            ],
        },
    },
]

WSGI_APPLICATION = "digi_kedmat.wsgi.application"
ASGI_APPLICATION = "digi_kedmat.asgi.application"

#### Database
DATABASES = {
    'default': eval(os.environ.get('DATABASE_INFO'))
}

#### IN MEMORY DBs : REDIS,  MEMCACHED , ...
try:
    CACHES = {
        "default": eval(os.environ.get('CACHE_INFO'))
    }
except:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    

### Channels Settings and Configs
if DEBUG:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

    
    
#### LOGGING SETTINGS AND CONFIGS
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "verbose": {
                "format": "{levelname} - {asctime} - {name} - {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/digi_khedmat_logs.log",
                "maxBytes":  1024*1024*50, # 50 MB
                "backupCount":  5,
                "formatter": "standard",
            },  
            "request_handler": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/django_requests.log",
                "maxBytes": 1024*1024*5, # 5 MB
                "backupCount": 5,
                "formatter": "standard",
            },
            "console": {
                "class": "logging.StreamHandler",
            },
            "barters_logger": {
                "level":"INFO",
                "class":"logging.handlers.RotatingFileHandler",
                "filename": "logs/barters_logs.log",
                "maxBytes": 1024*1024*5, # 5 MB
                "backupCount": 5,
                "formatter":"verbose",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "django": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["request_handler"],
                "level": "DEBUG",
                "propagate": False,
            },
            "watchman": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "barters": {
                "handlers": ["barters_logger",],
                "level": "INFO",
                "propagate": False,
            },
        },
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

#### Internationalization
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
TIME_ZONE = os.environ.get('TIME_ZONE')
USE_I18N = os.environ.get('USE_I18N')
USE_TZ = os.environ.get('USE_TZ')


#### Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('STATIC_URL')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
if DEBUG:
    STATIC_ROOT = eval(os.environ.get('STATIC_ROOT_DEV'))
else:
    STATIC_ROOT = os.environ.get('STATIC_ROOT')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)


##### TailwindCss Settings
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = which("npm")


# Compression settings and conf
COMPRESS_ENABLED = not DEBUG
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css':[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js':[
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
# COMPRESS_STORAGE = "staticfiles.storage.StaticFileStorage"
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False


# Media Files (image, video, ...)
MEDIA_URL = os.environ.get('MEDIA_URL')
if DEBUG:
    MEDIA_ROOT = eval(os.environ.get('MEDIA_ROOT_DEV'))
else:
    MEDIA_ROOT = os.environ.get('MEDIA_ROOT')


# default Auto Field
DEFAULT_AUTO_FIELD = os.environ.get('DEFAULT_AUTO_FIELD')


# Ckeditor Settings and Configs
CKEDITOR_BASEPATH = os.environ.get('CKEDITOR_BASEPATH')
CKEDITOR_UPLOAD_PATH = os.environ.get('CKEDITOR_UPLOAD_PATH')
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = os.environ.get("CKEDITOR_JQUERY_URL")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Custom": [
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            # {
            #     "name": "colors", 
            #     "items": [
            #         "TextColor", 
            #         "BGColor"
            #     ]
            # },
            {
                "name": "yourcustomtools",
                "items": [
                    # put the name of your editor.ui.addButton here
                    "Preview",
                    "Maximize",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                ],
            },
        ],
        "toolbar": "Custom",  # put selected toolbar config here
        "toolbarGroups": [
            {"name": "document", "groups": ["mode", "document", "doctools"]}
        ],
        "height": 400,
        # 'width': '100%',
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "devtools",
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
                "codesnippet",
            ]
        ),
    }
}



#### PhoneNumberField Configurations
PHONENUMBER_DEFAULT_REGION = os.environ.get('PHONENUMBER_DEFAULT_REGION')
PHONENUMBER_DEFAULT_FORMAT = os.environ.get('PHONENUMBER_DEFAULT_FORMAT')


#### CAPTCHA SETTINGS
CAPTCHA_LENGTH = 6
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'
CAPTCHA_BACKGROUND_COLOR = "#ffffff"
CAPTCHA_FOREGROUND_COLOR = "#000000"
CAPTCHA_LETTER_ROTATION = (-10,20)
CAPTCHA_IMAGE_SIZE = (200,60)
CAPTCHA_FONT_SIZE = 25
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',)
# CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)


#### WATCHMAN SETTINGS
WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'