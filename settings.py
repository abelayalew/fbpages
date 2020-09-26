import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        # Database driver
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}

INSTALLED_APPS = (
    'db',
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = os.environ.get('SECRET_KEY')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')