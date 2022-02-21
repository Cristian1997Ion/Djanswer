"""
ASGI config for Djanswer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

from game.routing import websocket_urlpatterns
from game.socket_consumers.utils import GAME_ENGINE_NAME
from game.socket_consumers.worker.game_engine_consumer import GameEngineConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djanswer.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    'channel': ChannelNameRouter({GAME_ENGINE_NAME: GameEngineConsumer.as_asgi()})
})