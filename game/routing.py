# chat/routing.py
from django.urls import re_path

from . import socket_consumers

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_code>\w+)/lobby$', socket_consumers.RoomLobbyConsumer.as_asgi()),
]