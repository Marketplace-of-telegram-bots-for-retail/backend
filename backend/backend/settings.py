from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='Secret-key')

DEBUG = config('DEBUG', default=False, cast=bool)

USE_SQLITE = config('USE_SQLITE', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

AUTH_USER_MODEL = 'users.User'

# fmt: off
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api.apps.ApiConfig',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'drf_spectacular',
    'debug_toolbar',
    'corsheaders',
]
# fmt: on

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB', default='django'),
            'USER': config('POSTGRES_USER', default='django_user'),
            'PASSWORD': config('POSTGRES_PASSWORD', default='django_password'),
            'HOST': config('DB_HOST', default='postgres'),
            'PORT': config('DB_PORT', default=5432),
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'

MEDIA_ROOT = config('MEDIA_ROOT', default=BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Список эндпоинтов API',
    'DESCRIPTION': (
        'Документация API. Ссылка на пояснение к документации: '
        'https://docs.google.com/document/d/1UYkoB6dfhXv4imFhy47Vkhyvi7T7azrro9MyQfczb8Y/edit?usp=sharing'
    ),
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

DJOSER = {
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user_create_password_retype': 'users.serializers.CustomUserCreatePasswordRetypeSerializer',
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    # 'SET_PASSWORD_RETYPE': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    # 'PERMISSIONS': {
    #     'user': ['rest_framework.permissions.AllowAny'],
    # },
    # 'USER_ID_FIELD': 'email',
    'LOGIN_FIELD': 'email',
}

PAGE_SIZE = 9

FIRST_ARTICLE = 100000

CSRF_TRUSTED_ORIGINS = [
    'https://botmarketplace.ru',
    'https://80.87.109.115',
    'http://localhost:3000',
    'https://marketplace-of-telegram-bots-for-retail.github.io',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://marketplace-of-telegram-bots-for-retail.github.io',
]

PROMOCODE = {
    'STUDENT_10': 10,
    'SCHOOL_20': 20,
    'BIRTHDAY_30': 30
}
