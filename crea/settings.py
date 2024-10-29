"""
Django settings for crea project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from pathlib import Path
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p=h!ot2ea=8=vco@i5wu9hg12*z0ha3d(yr$&3%za7qhrc_^ih'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crea_app',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'storages',
    'b2sdk',
    'profile_app',
    'forms',
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

ROOT_URLCONF = 'crea.urls'

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

WSGI_APPLICATION = 'crea.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crea',  
        'USER': 'crea_user',
        'PASSWORD': 'Gobu@0306',
        'HOST': 'localhost',
        'PORT': '3306',            
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
SHOW_SWAGGER = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'crea_app.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'connect@artiztnetwork.com'  # your email
EMAIL_HOST_PASSWORD = 'istz tnfx jjwy cslm'  # App Password if 2FA is enabled
DEFAULT_FROM_EMAIL = 'connect@artiztnetwork.com'



B2_ACCOUNT_ID = '0055668acec6f400000000007'  # Replace with your Account ID
B2_APPLICATION_KEY = 'K005CQRVl9H+5mxfqK0DE0MtezgziUU'  # Replace with your Application Key
B2_BUCKET_ID = 'f576e6c88aec9eec962f0410'
B2_FOLDER_NAME = 'onboarding-images'
B2_STORAGE_CLASS = 'crea_app.backblaze_storage.B2Storage'
B2_BUCKET_NAME = "crea-onboarding"
END_POINT_URL = "s3.us-east-005.backblazeb2.com"


# Configure default file storage
# DEFAULT_FILE_STORAGE = 'storages.backends.b2.B2Storage'

# Optional: Define your B2 file path if needed
DEFAULT_FILE_STORAGE = 'crea_app.backblaze_storage.BackblazeStorage'

DJANGO_SETTINGS_MODULE='crea.settings'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

# Load Firebase service account key
# Since serviceAccountKey.json is in the same directory as this script, we can get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This should point to the crea directory
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Check if the credential file exists
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"The service account key file does not exist at the path: {cred_path}")

# Initialize Firebase
try:
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")
except FirebaseError as e:
    print(f"Error initializing Firebase: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

def verify_google_token(google_token):
    try:
        decoded_token = auth.verify_id_token(google_token)
        return decoded_token  # Contains user info
    except auth.InvalidIdTokenError:
        return {"status": "error", "message": "Invalid Google token."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Example usage:
if __name__ == "__main__":
    # Replace 'your_google_token' with an actual token for testing
    google_token = 'your_google_token'
    verification_result = verify_google_token(google_token)
    print(verification_result)
