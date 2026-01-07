"""
Django settings for menu_backend project.
"""

import os
import dj_database_url
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-jkodbu2a^jg-te8c=ira-c^42@93w!n4^n=d!fj7_ob1gyarrb')

# SECURITY WARNING: don't run with debug turned on in production!
# Allow temporary enabling of DEBUG via environment variable `DJANGO_DEBUG`.
# Set `DJANGO_DEBUG=1` in Render to see tracebacks while debugging, then remove it.
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() in ('1', 'true', 'yes') or ('RENDER' not in os.environ)

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Para desarrollo local
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])    

# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'menu_backend.menu',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'menu_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'menu_backend.wsgi.application'

# Database
# If DATABASE_URL is set (e.g., Render with external DB), use it.
# Otherwise, fall back to SQLite (for local dev or Render free tier).
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600
        )
    }
else:
    # Fallback to SQLite for development and free tier deployments
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin customization
ADMIN_SITE_HEADER = "🍽️ QuickMenu Admin"
ADMIN_SITE_TITLE = "Panel de Control del Restaurante"
ADMIN_INDEX_TITLE = "Gestión del Menú Digital"

# CORS Configuration: leer desde variable de entorno `CORS_ALLOWED_ORIGINS`.
# Formato: "https://front.example.com,http://localhost:5173"
_env_cors = os.environ.get('CORS_ALLOWED_ORIGINS')
if _env_cors:
    CORS_ALLOWED_ORIGINS = [h.strip() for h in _env_cors.split(',') if h.strip()]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://restaurante-eli.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ]
CORS_ALLOW_CREDENTIALS = True

# Permitir todos los orígenes temporalmente si la variable de entorno lo solicita
# Uso recomendado: establecer CORS_ALLOW_ALL_ORIGINS=1 solo para debugging.
if os.environ.get('CORS_ALLOW_ALL_ORIGINS', '').lower() in ('1', 'true', 'yes'):
    CORS_ALLOW_ALL_ORIGINS = True

# Expresiones regulares útiles para aceptar orígenes de plataformas como Vercel/Render
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?://.*\.vercel\.app$",
    r"^https?://.*\.onrender\.com$",
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# Render production settings
if 'RENDER' in os.environ:
    # Security settings
    SECURE_HSTS_SECONDS = 31536000
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Allowed hosts
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('sabor-y-arte.onrender.com')