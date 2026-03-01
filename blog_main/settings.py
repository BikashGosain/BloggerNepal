from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------
# SECURITY
# ---------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost,your-app.onrender.com'
).split(',')

CSRF_TRUSTED_ORIGINS = [
    "https://your-app.onrender.com"
]

SITE_ID = int(os.getenv('DJANGO_SITE_ID', 1))

# ---------------------
# INSTALLED APPS
# ---------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'crispy_forms',
    'crispy_bootstrap4',
    'ckeditor',
    'ckeditor_uploader',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    'blogs',
    'about_us',
    'contact',
    'dashboards',
    'social_links',
    'follow_following',

    'rest_framework',

    'cloudinary',
    'cloudinary_storage',
]

# ---------------------
# FILE STORAGE (Cloudinary)
# ---------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# MEDIA_URL is handled by Cloudinary
MEDIA_URL = '/media/'  # optional placeholder, Cloudinary serves files directly

# ---------------------
# REST FRAMEWORK
# ---------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"]
}

# ---------------------
# AUTHENTICATION
# ---------------------
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ---------------------
# MIDDLEWARE
# ---------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'blog_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom processors
                'blogs.context_processors.get_categories',
                'blogs.context_processors.get_social_links',
                'blogs.context_processors.user_roles',
                'blogs.context_processors.unread_notifications_count',
                'follow_following.context_processors.follow_counts',
                'follow_following.context_processors.user_following_ids',
                'follow_following.context_processors.followers_list',
                'follow_following.context_processors.following_list',
                'blogs.context_processors.latestpost',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_main.wsgi.application'

# ---------------------
# DATABASE
# ---------------------
# this databse for connecting render postgres database using DATABASE_URL from .env file

DATABASES = {
    'default': {
        **dj_database_url.config(default=os.getenv('DATABASE_URL')),
        'OPTIONS': {
            'options': '-c search_path=project2'
        }
    }
}

# this is for deployment in render.com, render.com automatically sets DATABASE_URL environment variable
# but i have also added individual database settings in .env file for local development and testing, so if DATABASE_URL is not set, it will fallback to individual settings

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DJANGO_DB_ENGINE', 'django.db.backends.postgresql'),
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT', 5432),
#     }
# }

# ---------------------
# PASSWORD VALIDATION
# ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------
# INTERNATIONALIZATION
# ---------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# ---------------------
# STATIC FILES
# ---------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'blog_main' / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------
# CKEDITOR CONFIG
# ---------------------
CRISPY_TEMPLATE_PACK = "bootstrap4"

CKEDITOR_UPLOAD_PATH = ""  # handled by Cloudinary
CKEDITOR_ALLOW_NONIMAGE_FILES = True
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    }
}

# ---------------------
# EMAIL SETTINGS
# ---------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ---------------------
# ALLAUTH SETTINGS
# ---------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_SECRET'),
        },
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_ADAPTER = 'blog_main.adapters.MySocialAccountAdapter'
