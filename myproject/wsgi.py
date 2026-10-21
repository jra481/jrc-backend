"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Keep an optional migration safety net for platforms that start the WSGI
# module directly. AWS EC2 uses a dedicated release step and sets this
# to false so multiple Gunicorn workers never race to migrate on boot.
django.setup()
if os.getenv("RUN_MIGRATIONS_ON_START", "true").lower() in (
    "true",
    "1",
    "t",
    "yes",
    "on",
):
    call_command("migrate", interactive=False, verbosity=0)

application = get_wsgi_application()
