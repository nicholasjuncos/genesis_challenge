"""
WSGI config for genesis_code project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from decouple import config as env, UndefinedValueError

from django.core.wsgi import get_wsgi_application

try:
    if env('ENVIRONMENT') == 'production':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
except UndefinedValueError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()
