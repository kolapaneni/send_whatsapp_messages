import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-enst*gphj=&2^53@%_l8kj(k^82f*yu@zx9yi4@uyy495coh1)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = 'room/'
LOGIN_URL = 'login/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'core',
    'room',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangochat.urls'

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

WSGI_APPLICATION = 'djangochat.wsgi.application'
ASGI_APPLICATION = 'djangochat.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    }
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chatbot',
        'USER': 'chatbot',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TWILIO_ACCOUNT_SID = 'ACf277df7c17901f4619a31059a7f05bcf'
TWILIO_AUTH_TOKEN = 'e672cd098b50c4b70ad961cf99c4f32a'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email.host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'balaking137@gmail.com'
EMAIL_HOST_PASSWORD = '9966787981'
DEFAULT_FROM_EMAIL = 'balaking137@gmail.com'

# LOGIN_REDIRECT_URL = 'dashboard'
# LOGIN_URL = 'login'


#--------- WHATSAPP API PROVIDED BY THE FACEBOOK META----------------
WHATSAPP_URL = "https://graph.facebook.com/v15.0/100722319578564/messages"
WHATSAPP_TOKEN = "Bearer EAAMzLHHR9hcBAHPXZAuUfiv6JRfZASkguZClFJsS5s9gWZAL41uoIhYUb2GDUARPoir8BCefDFLa7oBwbCp7QK3nXcNfYadyFaXZBDtD0btSOQHCfX9AiCxilUFO3HRDJVe4q65i7VWxTB1WqMmtkwR5H3RCIYdjsR95WP7MQWTENQwnzJtScwBeme0fFWAAN8hXkhxAqswZDZD"

WEBHOOK_VERIFY_TOKEN = '1d731114-f447-4e87-b43e-8e858414ef95'


#--------- WHATSPP API PROVIDED BY THE INFOBIP------------------
INFOBIP_URL = "https://pw6wq8.api.infobip.com"
INFOBIP_API_KEY = "App eda012762988ae35ebcc7f02b3a19d1c-9e22ba27-709b-4ae0-905b-c8a042f5b89c"

