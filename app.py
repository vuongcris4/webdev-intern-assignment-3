"""Legacy compatibility entrypoint for the Django application."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def create_app():
    """Return a WSGI application for compatibility with old tooling."""
    return get_wsgi_application()


application = create_app()
