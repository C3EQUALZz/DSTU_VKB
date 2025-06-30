"""
WSGI config for OmniDB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from . import startup

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pgmanage.settings")

application = get_wsgi_application()

# Startup Procedure
#startup.startup_procedure()
