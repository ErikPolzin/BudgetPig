"""
WSGI config for budgetPig project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

path = os.path.expanduser('~/budgetPig')
if path not in sys.path and os.path.exists(path):
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'budgetPig.settings'

application = StaticFilesHandler(get_wsgi_application())
