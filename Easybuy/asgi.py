
from asyncio import protocols
from asyncio.base_events import _ProtocolFactory
from multiprocessing import AuthenticationError
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Easybuy.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
        )
    )
})
