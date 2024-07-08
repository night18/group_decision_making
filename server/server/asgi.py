"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import experiment.routing
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
	"http": django_asgi_app,
	"websocket": AuthMiddlewareStack(
		URLRouter(
			experiment.routing.websocket_urlpatterns
		)
	)
})
