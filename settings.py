import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        # Database driver
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.environ.get('DB_NAME'),
        # 'USER': os.environ.get('DB_USER'),
        # 'PASSWORD': os.environ.get('DB_PASSWORD'),
        # 'HOST': os.environ.get('DB_HOST'),
        # 'PORT': os.environ.get('DB_PORT')
    }
}

INSTALLED_APPS = (
    'db',
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "os.environ.get('SECRET_KEY')"
