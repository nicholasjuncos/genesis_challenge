from .base import *
from dj_database_url import parse as db_url

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env('SECRET_KEY', default='$^jxe7=ujsxid8_n(i#zg5%^2d+1zb5*6+u46$p4p9i=+-dkz$')

# mailhog config
EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'

# Cors Headers setup (May not be needed for this project)
# ------------------------------------------------------------------------------
# MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ] + MIDDLEWARE
# INSTALLED_APPS += [ 'corsheaders', ]

# ALLOWED_HOSTS CONFIG
ALLOWED_HOSTS = [
    '0.0.0.0',
    'localhost',
    '127.0.0.1',
]

# DATABASE CONFIG
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# https://pypi.org/project/python-decouple/#example-how-do-i-use-it-with-django
DATABASES = {
    'default': env('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'), cast=db_url)
}

# May not bee needed for this project
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:4200',
#     'http://localhost:8080',
# ]
