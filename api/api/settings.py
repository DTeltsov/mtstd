import ast
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'b0s1z6!ks27aa01^r%ac!^&x2uff6cp*5+eai^zu2x9i(_ia$(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'debug_toolbar',
    'music',
    'auth_api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI_APPLICATION = 'api.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'production'),
        'USER': os.environ.get('DB_USER_NAME', 'root'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD', '123'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get("DB_PORT", '3336'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'ssl': {"verify_mode": None},
        },
    }
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # for response data
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

INTERNAL_IPS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 500,
    'HTML_SELECT_CUTOFF': 100,
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Docs',
    'VERSION': '1.0.0',

    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
        "filter": True,
        "displayOperationId": True,
    },
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'SERVE_PUBLIC': False,
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
        'api.swagger.postprocess'
    ],
}

AUTHENTICATION_BACKENDS = [
    'auth_api.backend_auth_user.BackendAuth',
    # 'django.contrib.auth_api.backends.ModelBackend',
]
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'auth_api.AccountUser'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(name) %(message)s "
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': "json",
        },
    },
    'loggers': {
        'api.measures': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
            'propagate': False,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

# DJANGO_JSON_EDITOR_STYLE
JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.10.2/jsoneditor.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.10.2/jsoneditor.min.css'


SESSION_COOKIE_SECURE = ast.literal_eval(os.environ.get("SESSION_COOKIE_SECURE", "None"))  # True
CSRF_COOKIE_SECURE = ast.literal_eval(os.environ.get("CSRF_COOKIE_SECURE", "None"))  # True
SECURE_PROXY_SSL_HEADER = ast.literal_eval(os.environ.get("SECURE_PROXY_SSL_HEADER", "None")) # ('HTTP_X_FORWARDED_PROTO', 'https')

# Using django-storages
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_SIGNATURE_VERSION = os.environ.get("AWS_S3_SIGNATURE_VERSION", default="s3v4")
# https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
AWS_DEFAULT_ACL = os.environ.get("AWS_DEFAULT_ACL", default="private")
AWS_PRESIGNED_EXPIRY = os.environ.get("AWS_PRESIGNED_EXPIRY", default=10)  # seconds

AWS_S3_ENDPOINT_URL = os.environ.get("ENDPOINT_AWS_S3", None)

# hard code set AWS permission bucket and region
if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = "songs"
    AWS_S3_REGION_NAME = "eu-west-1"
else:
    AWS_STORAGE_BUCKET_NAME = "songs"
    AWS_S3_REGION_NAME = "eu-west-3"
