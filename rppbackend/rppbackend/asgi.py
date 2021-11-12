"""
ASGI config for rppbackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
import chat.routing
from channels.auth import AuthMiddlewareStack

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rppbackend.settings')
django.setup()

application = ProtocolTypeRouter({
    #"http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
            URLRouter(
                    chat.routing.websocket_urlpatterns
                )
        )
})
