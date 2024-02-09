import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import re_path
from chat.consumers import ChatConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digi_khedmat.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r'ws/chat/(?P<room_name>[\w-]+)/$', ChatConsumer.as_asgi()),
                ]
            )
        )
    )
})
