"""
ASGI config for DjangoRed project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
"""
from channels.auth import AuthMiddlewareStack

from channels.routing import URLRouter
"""
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import os
import VisualizationApp.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRed.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application()
})
