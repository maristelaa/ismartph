"""
WSGI config for ismartproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('C:\\Users\\angie\\OneDrive\\Documents\\GitHub\\ismartph\\ismartproject')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ismartproject.settings')

application = get_wsgi_application()
