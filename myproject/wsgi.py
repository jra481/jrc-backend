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

# Some Render services have an explicit dashboard start command that bypasses
# the repository Procfile. Keep the database schema current in that case too.
# This is idempotent and can be disabled for deployments that run migrations
# through a dedicated release step with RUN_MIGRATIONS_ON_START=false.
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
