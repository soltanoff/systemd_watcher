# from .settings import INSTALLED_APPS, MIDDLEWARE
# Uncomment first line for development server
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'Your secret key'
DEBUG = True  # False if your want to use in production
ALLOWED_HOSTS = ['*']  # for docker-compose


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mydb',
#         'USER': 'dbuser',
#         'PASSWORD': 'dbpassword',
#         'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8',
#             'use_unicode': True,
#         },
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# if you want to use debug_toolbar (dev server only)
# INSTALLED_APPS.append('debug_toolbar')
# MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
