"""
WSGI config for blog_main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_main.settings')

application = get_wsgi_application()


try:
    import create_superuser_on_startup
except Exception as e:
    print("Superuser creation skipped:", e)


try:
    import create_groups_on_startup
except Exception as e:
    print("Groups creation skipped:", e)
