import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-qa$y3ax(qz(v4b4d#=qv)&x=6$1==ga_5n@mch@6rh=wp&lz*h')

# SECURITY WARNING: don't run with debug turned on in production!
# Automatically switches to False on Render if you set the environment variable DEBUG=False
DEBUG = os.environ.get('DEBUG', 'False') == 'False'

# 1. ALLOWED HOSTS
# We explicitly add your Render domain and a wildcard for safety.
ALLOWED_HOSTS = [
    'ecommerce-website-y9id.onrender.com',
    'localhost',
    '127.0.0.1',
    '*'
]

# Helper to capture Render's dynamic hostname
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# 2. CSRF TRUSTED ORIGINS
# Required for Django 4.0+ to prevent 403 errors when logging into Admin on Render
CSRF_TRUSTED_ORIGINS = ['https://ecommerce-website-y9id.onrender.com']


# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Jazzmin must stay at the top
    'products',
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Vital for serving CSS/JS on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database - Note: SQLite will reset on every Render deploy/restart
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Jazzmin Amazon-Style Admin Settings
JAZZMIN_SETTINGS = {
    "site_title": "Hyper Seller Central",
    "site_header": "Hyper Admin",
    "site_brand": "⚡ HYPER",
    "welcome_sign": "Inventory Control Center",
    "copyright": "Hyper Store Ltd",
    "search_model": ["products.Product"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "products.Product": "fas fa-box",
        "products.Order": "fas fa-shipping-fast",
        "accounts.User": "fas fa-users",
    },
}

JAZZMIN_UI_CONFIG = {
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "sidebar": "sidebar-dark-primary",
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 3. STATIC FILES CONFIGURATION (WhiteNoise)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Use Manifest storage to compress files and handle caching automatically
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication Redirects
LOGIN_REDIRECT_URL = 'products'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'