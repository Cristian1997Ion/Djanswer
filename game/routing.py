# chat/routing.py
from django.urls import re_path

import game.socket_consumers.client as client

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_code>\w+)/lobby$', client.RoomLobbyConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_code>\w+)/lobby/owner$', client.RoomLobbyOwnerConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_code>\w+)/game$', client.RoomGameConsumer.as_asgi()),
]