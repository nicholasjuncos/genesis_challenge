"""
ASGI config for genesis_code project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from decouple import config as env, UndefinedValueError

from django.core.asgi import get_asgi_application

try:
    if env('ENVIRONMENT') == 'production':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
except UndefinedValueError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
