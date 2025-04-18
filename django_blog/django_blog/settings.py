import os
import sys
import logging

from pathlib import Path
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY_ENV"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

SITE_ID = 1

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "mptt",
    "bootstrap5",
    "debug_toolbar",
    "django_mptt_admin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.blog.apps.BlogConfig",
    "apps.accounts",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "rest_framework",
    "apps.django_blog_api",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_filters",
    "taggit",
    "django_recaptcha",
    "django_ckeditor_5",
    "guardian",
    "rosetta",
    "django.contrib.postgres",
    "markdownx",
    "django_celery_beat",
    "django_celery_results",
]

RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHA_PUBLIC_KEY_ENV"))
RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHA_PRIVATE_KEY_ENV"))

STATIC_ROOT = BASE_DIR / "static/"
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload',
                   'undo', 'redo'],
        'height': '300px',
        'width': '100%',
    },
}

CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_UPLOAD_PATH = 'uploads/'
CKEDITOR_5_CUSTOM_CSS = 'path-to-your-custom.css'  # Optional custom CSS


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": (BASE_DIR / "cache"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Django_Blog API",
    "DESCRIPTION": "A sample blog to learn about DRF",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Middleware django-debug-toolbar
    "apps.accounts.middleware.ActiveUserMiddleware",
]

ROOT_URLCONF = "django_blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_blog.wsgi.application"

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Celery Beat Settings
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# SQlite
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.getenv("NAME_POSTGRES")),
        "USER": str(os.getenv("USER_POSTGRES")),
        "PASSWORD": str(os.getenv("PASSWORD_POSTGRES")),
        "HOST": str(os.getenv("HOST_POSTGRES")),
        "PORT": str(os.getenv("PORT_POSTGRES")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "templates/js/"]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Этот бэкенд Django использует по умолчанию
    "guardian.backends.ObjectPermissionBackend",  # А это  бэкенд django_guardian
)


CELERY_BROKER_URL = (
    "redis://localhost:6379"  # указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
)
CELERY_RESULT_BACKEND = "redis://localhost:6379"  # указывает на хранилище результатов выполнения задач.
CELERY_ACCEPT_CONTENT = ["application/json"]  # допустимый формат данных.
CELERY_TASK_SERIALIZER = "json"  # метод сериализации задач.
CELERY_RESULT_SERIALIZER = "json"  # метод сериализации результатов.

# Настройки Flower
FLOWER_BASIC_AUTH = ['admin:admin']  # Базовая аутентификация для доступа к Flower
FLOWER_PORT = 5555  # Порт, на котором будет запущен Flower
FLOWER_URL_PREFIX = 'flower'  # URL префикс для Flower
FLOWER_PERSISTENT = True  # Сохранение состояния между перезапусками
FLOWER_STATE_SAVE_INTERVAL = 3600000  # Интервал сохранения состояния (в миллисекундах)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"


ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = str(os.getenv("EMAIL_HOST_ENV"))
EMAIL_PORT = 465
EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER_ENV"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD_ENV"))
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = str(os.getenv("DEFAULT_FROM_EMAIL_ENV"))
SERVER_EMAIL = str(os.getenv("SERVER_EMAIL_ENV"))
ADMINS = str(os.getenv("ADMINS_ENV"))
EMAIL_SUBJECT_PREFIX = str(os.getenv("EMAIL_SUBJECT_PREFIX_ENV"))

# В вашем settings.py
ADMINS = [('NikitaTichonow', 'nik7674@yandex.ru')]



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
        "file_general": {"format": "%(asctime)s - %(levelname)s - %(module)s - %(message)s"},
        "file_errors": {
            "format": "%(asctime)s - %(levelname)s - %(message)s - %(pathname)s",
        },
        "file_security": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        },
    },
    "filters": {
        "debug_only": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: settings.DEBUG,
        },
        "production_only": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: not settings.DEBUG,
        },
    },
    "handlers": {
        "file_general": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/general.log"),
            "formatter": "file_general",
            "filters": ["production_only"],
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/errors.log"),
            "formatter": "file_errors",
        },
        "file_security": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/security.log"),
            "formatter": "file_security",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "file_errors",
            "filters": ["production_only"],
        },
    },
    "loggers": {
        # Основной логгер Django
        "django": {
            "handlers": ["file_general", "file_errors", "file_security"],
            "level": "DEBUG",
            "propagate": True,
        },
        # Логгер для запросов
        "django.request": {
            "handlers": ["mail_admins", "file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
        # Логгер для сервера
        "django.server": {
            "handlers": ["mail_admins", "file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
        # Логгер для шаблонов
        "django.template": {
            "handlers": ["file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
        # Логгер для базы данных
        "django.db.backends": {
            "handlers": ["file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
        # Логгер для безопасности
        "django.security": {
            "handlers": ["file_security"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
